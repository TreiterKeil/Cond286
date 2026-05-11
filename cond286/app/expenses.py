from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from datetime import datetime, date
from app.utils.decorators import admin_required
from app.utils.helpers import format_currency
from app.models import Despesa, MovimentoBanco
from app import db

expenses_bp = Blueprint('expenses', __name__)


@expenses_bp.route('/expenses')
@login_required
@admin_required
def list():
    despesas = Despesa.query.order_by(Despesa.data.desc()).all()
    return render_template('expenses/list.html', despesas=despesas, format_currency=format_currency)


@expenses_bp.route('/expenses/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new():
    categorias = [
        'Electricidade',
        'Água',
        'Telecomunicações',
        'Limpeza',
        'Manutenção',
        'Comissão Bancária',
        'Seguro',
        'Material Escritório',
        'Ferramentas/Utensílios',
        'Outra'
    ]

    if request.method == 'POST':
        categoria = request.form.get('categoria')
        descricao = request.form.get('descricao')
        valor = request.form.get('valor')
        data_despesa = request.form.get('data')
        metodo_pagamento = request.form.get('metodo_pagamento')
        pago_por = request.form.get('pago_por')
        notas = request.form.get('notas')

        errors = []
        if not categoria:
            errors.append('Selecione uma categoria.')
        if not descricao:
            errors.append('Introduza uma descrição.')
        if not valor or float(valor) <= 0:
            errors.append('Introduza um valor válido.')
        if not data_despesa:
            errors.append('Selecione a data da despesa.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('expenses/new.html', categorias=categorias)

        despesa = Despesa(
            categoria=categoria,
            descricao=descricao,
            valor=float(valor),
            data=datetime.strptime(data_despesa, '%Y-%m-%d').date(),
            metodo_pagamento=metodo_pagamento if metodo_pagamento else None,
            pago_por=pago_por if pago_por else None,
            reembolsado=(pago_por == 'Administrador (pessoal)'),
            notas=notas if notas else None
        )

        db.session.add(despesa)
        db.session.commit()

        flash(f'Despesa "{descricao}" registada com sucesso!', 'success')
        return redirect(url_for('expenses.list'))

    return render_template('expenses/new.html', categorias=categorias, today=date.today())


@expenses_bp.route('/expenses/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    despesa = Despesa.query.get_or_404(id)
    categorias = [
        'Electricidade',
        'Água',
        'Telecomunicações',
        'Limpeza',
        'Manutenção',
        'Comissão Bancária',
        'Seguro',
        'Material Escritório',
        'Ferramentas/Utensílios',
        'Outra'
    ]

    if request.method == 'POST':
        categoria = request.form.get('categoria')
        descricao = request.form.get('descricao')
        valor = request.form.get('valor')
        data_despesa = request.form.get('data')
        metodo_pagamento = request.form.get('metodo_pagamento')
        pago_por = request.form.get('pago_por')
        notas = request.form.get('notas')

        errors = []
        if not categoria:
            errors.append('Selecione uma categoria.')
        if not descricao:
            errors.append('Introduza uma descrição.')
        if not valor or float(valor) <= 0:
            errors.append('Introduza um valor válido.')
        if not data_despesa:
            errors.append('Selecione a data da despesa.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('expenses/edit.html', despesa=despesa, categorias=categorias)

        despesa.categoria = categoria
        despesa.descricao = descricao
        despesa.valor = float(valor)
        despesa.data = datetime.strptime(data_despesa, '%Y-%m-%d').date()
        despesa.metodo_pagamento = metodo_pagamento if metodo_pagamento else None
        despesa.pago_por = pago_por if pago_por else None
        despesa.reembolsado = (pago_por == 'Administrador (pessoal)')
        despesa.notas = notas if notas else None

        db.session.commit()

        flash(f'Despesa "{descricao}" atualizada com sucesso!', 'success')
        return redirect(url_for('expenses.list'))

    return render_template('expenses/edit.html', despesa=despesa, categorias=categorias)


@expenses_bp.route('/expenses/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete(id):
    despesa = Despesa.query.get_or_404(id)
    descricao = despesa.descricao
    
    # Remove bank reconciliation links first
    MovimentoBanco.query.filter_by(despesa_id=id).update(
        {MovimentoBanco.despesa_id: None, MovimentoBanco.reconciliado: False}
    )
    
    db.session.delete(despesa)
    db.session.commit()

    flash(f'Despesa "{descricao}" eliminada.', 'info')
    return redirect(url_for('expenses.list'))