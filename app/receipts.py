from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from app.utils.decorators import admin_required
from app.utils.helpers import format_currency, gerar_numero_recibo
from app.models import Recibo, Unidade, MovimentoBanco
from app import db

receipts_bp = Blueprint('receipts', __name__)


@receipts_bp.route('/receipts')
@login_required
@admin_required
def list():
    recibos = Recibo.query.order_by(Recibo.numero.desc()).all()
    return render_template('receipts/list.html', recibos=recibos, format_currency=format_currency)


@receipts_bp.route('/receipts/<int:id>/print')
@login_required
@admin_required
def print_receipt(id):
    recibo = Recibo.query.get_or_404(id)
    return render_template('receipts/print.html', recibo=recibo, format_currency=format_currency)


@receipts_bp.route('/receipts/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new():
    unidades = Unidade.query.filter_by(ativo=True).order_by(Unidade.codigo).all()

    if request.method == 'POST':
        unidade_id = request.form.get('unidade_id')
        valor = request.form.get('valor')
        periodo_inicio = request.form.get('periodo_inicio')
        periodo_fim = request.form.get('periodo_fim')
        metodo_pagamento = request.form.get('metodo_pagamento')
        data_recebido = request.form.get('data_recebido')
        notas = request.form.get('notas')

        # Validation
        errors = []
        if not unidade_id:
            errors.append('Selecione uma fração.')
        if not valor or float(valor) <= 0:
            errors.append('Introduza um valor válido.')
        if not periodo_inicio:
            errors.append('Selecione a data de início do período.')
        if not periodo_fim:
            errors.append('Selecione a data de fim do período.')
        if not data_recebido:
            errors.append('Selecione a data de recebimento.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('receipts/new.html', unidades=unidades)

        # Create receipt
        recibo = Recibo(
            numero=gerar_numero_recibo(),
            unidade_id=int(unidade_id),
            valor=float(valor),
            periodo_inicio=datetime.strptime(periodo_inicio, '%Y-%m-%d').date(),
            periodo_fim=datetime.strptime(periodo_fim, '%Y-%m-%d').date(),
            metodo_pagamento=metodo_pagamento,
            data_recebido=datetime.strptime(data_recebido, '%Y-%m-%d').date(),
            notas=notas if notas else None
        )

        db.session.add(recibo)
        db.session.commit()

        flash(f'Recibo nº {recibo.numero} criado com sucesso!', 'success')
        return redirect(url_for('receipts.list'))

    return render_template('receipts/new.html', unidades=unidades, today=date.today())


@receipts_bp.route('/receipts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    recibo = Recibo.query.get_or_404(id)
    unidades = Unidade.query.filter_by(ativo=True).order_by(Unidade.codigo).all()

    if request.method == 'POST':
        unidade_id = request.form.get('unidade_id')
        valor = request.form.get('valor')
        periodo_inicio = request.form.get('periodo_inicio')
        periodo_fim = request.form.get('periodo_fim')
        metodo_pagamento = request.form.get('metodo_pagamento')
        data_recebido = request.form.get('data_recebido')
        notas = request.form.get('notas')

        errors = []
        if not unidade_id:
            errors.append('Selecione uma fração.')
        if not valor or float(valor) <= 0:
            errors.append('Introduza um valor válido.')
        if not periodo_inicio:
            errors.append('Selecione a data de início do período.')
        if not periodo_fim:
            errors.append('Selecione a data de fim do período.')
        if not data_recebido:
            errors.append('Selecione a data de recebimento.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('receipts/edit.html', recibo=recibo, unidades=unidades)

        recibo.unidade_id = int(unidade_id)
        recibo.valor = float(valor)
        recibo.periodo_inicio = datetime.strptime(periodo_inicio, '%Y-%m-%d').date()
        recibo.periodo_fim = datetime.strptime(periodo_fim, '%Y-%m-%d').date()
        recibo.metodo_pagamento = metodo_pagamento
        recibo.data_recebido = datetime.strptime(data_recebido, '%Y-%m-%d').date()
        recibo.notas = notas if notas else None

        db.session.commit()

        flash(f'Recibo nº {recibo.numero} atualizado com sucesso!', 'success')
        return redirect(url_for('receipts.list'))

    return render_template('receipts/edit.html', recibo=recibo, unidades=unidades)


@receipts_bp.route('/receipts/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete(id):
    recibo = Recibo.query.get_or_404(id)
    numero = recibo.numero
    
    # Remove bank reconciliation links first
    MovimentoBanco.query.filter_by(recibo_id=id).update(
        {MovimentoBanco.recibo_id: None, MovimentoBanco.reconciliado: False}
    )
    
    db.session.delete(recibo)
    db.session.commit()

    flash(f'Recibo nº {numero} eliminado.', 'info')
    return redirect(url_for('receipts.list'))