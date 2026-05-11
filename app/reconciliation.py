from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from datetime import datetime, date
from app.utils.decorators import admin_required
from app.utils.helpers import format_currency
from app.models import MovimentoBanco, Recibo, Despesa
from app import db

reconciliation_bp = Blueprint('reconciliation', __name__)


@reconciliation_bp.route('/reconciliation')
@login_required
@admin_required
def index():
    movimentos = MovimentoBanco.query.order_by(MovimentoBanco.data_movimento.desc()).all()
    
    reconciliados = sum(1 for m in movimentos if m.reconciliado)
    total = len(movimentos)
    
    # Get unreconciled items
    nao_reconciliados = [m for m in movimentos if not m.reconciliado]
    
    return render_template('reconciliation/index.html',
                           movimentos=movimentos,
                           reconciliados=reconciliados,
                           total=total,
                           nao_reconciliados=nao_reconciliados,
                           format_currency=format_currency)


@reconciliation_bp.route('/reconciliation/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new():
    if request.method == 'POST':
        data_movimento = request.form.get('data_movimento')
        data_valor = request.form.get('data_valor')
        descricao = request.form.get('descricao')
        montante = request.form.get('montante')
        saldo_apos = request.form.get('saldo_apos')

        errors = []
        if not data_movimento:
            errors.append('Introduza a data do movimento.')
        if not descricao:
            errors.append('Introduza uma descrição.')
        if not montante:
            errors.append('Introduza o montante.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('reconciliation/new.html')

        movimento = MovimentoBanco(
            data_movimento=datetime.strptime(data_movimento, '%Y-%m-%d').date(),
            data_valor=datetime.strptime(data_valor, '%Y-%m-%d').date() if data_valor else datetime.strptime(data_movimento, '%Y-%m-%d').date(),
            descricao=descricao,
            montante=float(montante),
            saldo_apos=float(saldo_apos) if saldo_apos else None
        )

        db.session.add(movimento)
        db.session.commit()

        flash('Movimento bancário adicionado!', 'success')
        return redirect(url_for('reconciliation.index'))

    return render_template('reconciliation/new.html', today=date.today())


@reconciliation_bp.route('/reconciliation/<int:id>/match', methods=['POST'])
@login_required
@admin_required
def match(id):
    movimento = MovimentoBanco.query.get_or_404(id)
    tipo = request.form.get('tipo')
    item_id = request.form.get('item_id')

    if tipo == 'recibo':
        movimento.recibo_id = int(item_id) if item_id else None
        movimento.despesa_id = None
        movimento.reconciliado = True
    elif tipo == 'despesa':
        movimento.despesa_id = int(item_id) if item_id else None
        movimento.recibo_id = None
        movimento.reconciliado = True
    elif tipo == 'ignorar':
        movimento.reconciliado = True
        movimento.recibo_id = None
        movimento.despesa_id = None

    db.session.commit()
    flash('Movimento reconciliado!', 'success')
    return redirect(url_for('reconciliation.index'))


@reconciliation_bp.route('/reconciliation/<int:id>/unmatch', methods=['POST'])
@login_required
@admin_required
def unmatch(id):
    movimento = MovimentoBanco.query.get_or_404(id)
    movimento.reconciliado = False
    movimento.recibo_id = None
    movimento.despesa_id = None
    db.session.commit()
    flash('Reconciliação desfeita.', 'info')
    return redirect(url_for('reconciliation.index'))

@reconciliation_bp.route('/reconciliation/<int:id>/match-form')
@login_required
@admin_required
def match_form(id):
    movimento = MovimentoBanco.query.get_or_404(id)
    
    # Get unreconciled receipts and expenses for matching
    recibos = Recibo.query.filter(
        ~Recibo.movimentos_banco.any()
    ).order_by(Recibo.numero.desc()).all()
    
    despesas = Despesa.query.filter(
        ~Despesa.movimentos_banco.any()
    ).order_by(Despesa.data.desc()).all()
    
    return render_template('reconciliation/match.html',
                           movimento=movimento,
                           recibos=recibos,
                           despesas=despesas,
                           format_currency=format_currency)