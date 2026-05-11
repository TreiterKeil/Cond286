from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from datetime import datetime, date
from app.utils.decorators import admin_required
from app.utils.helpers import format_currency
from app.models import MovimentoCaixa
from app import db

petty_cash_bp = Blueprint('petty_cash', __name__)


@petty_cash_bp.route('/petty-cash')
@login_required
@admin_required
def index():
    movimentos = MovimentoCaixa.query.order_by(MovimentoCaixa.data.desc()).all()
    
    # Calculate balance
    levantamentos = sum(m.valor for m in movimentos if m.tipo == 'levantamento')
    despesas = sum(m.valor for m in movimentos if m.tipo == 'despesa')
    saldo = levantamentos - despesas
    
    return render_template('petty_cash/index.html', 
                           movimentos=movimentos, 
                           saldo=saldo,
                           format_currency=format_currency)


@petty_cash_bp.route('/petty-cash/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        valor = request.form.get('valor')
        descricao = request.form.get('descricao')
        data_movimento = request.form.get('data')

        errors = []
        if not tipo:
            errors.append('Selecione o tipo de movimento.')
        if not valor or float(valor) <= 0:
            errors.append('Introduza um valor válido.')
        if not descricao:
            errors.append('Introduza uma descrição.')
        if not data_movimento:
            errors.append('Selecione a data.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('petty_cash/new.html')

        movimento = MovimentoCaixa(
            tipo=tipo,
            valor=float(valor),
            descricao=descricao,
            data=datetime.strptime(data_movimento, '%Y-%m-%d').date()
        )

        db.session.add(movimento)
        db.session.commit()

        tipo_texto = 'Levantamento' if tipo == 'levantamento' else 'Despesa de caixa'
        flash(f'{tipo_texto} registado com sucesso!', 'success')
        return redirect(url_for('petty_cash.index'))

    return render_template('petty_cash/new.html', today=date.today())