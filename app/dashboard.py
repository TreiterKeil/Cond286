from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import admin_required
from app.utils.helpers import format_currency
from app.models import Unidade, Recibo, Despesa, MovimentoCaixa, Configuracao
from datetime import date
from app import db

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
@admin_required
def index():
    hoje = date.today()
    primeiro_dia_mes = date(hoje.year, hoje.month, 1)
    primeiro_dia_ano = date(hoje.year, 1, 1)

    # Bank balance from settings or calculated
    config_saldo = Configuracao.query.filter_by(chave='saldo_inicial_banco').first()
    saldo_inicial = float(config_saldo.valor) if config_saldo else 2995.83

    # All income ever recorded
    total_receitas = db.session.query(db.func.sum(Recibo.valor)).scalar() or 0.0

    # All expenses ever recorded
    total_despesas = db.session.query(db.func.sum(Despesa.valor)).scalar() or 0.0

    # Calculated balance
    saldo_banco = saldo_inicial + total_receitas - total_despesas

    # Monthly income
    receitas_mes = db.session.query(db.func.sum(Recibo.valor))\
        .filter(Recibo.data_recebido >= primeiro_dia_mes)\
        .scalar() or 0.0

    # Monthly expenses
    despesas_mes = db.session.query(db.func.sum(Despesa.valor))\
        .filter(Despesa.data >= primeiro_dia_mes)\
        .scalar() or 0.0

    # Yearly totals
    receitas_ano = db.session.query(db.func.sum(Recibo.valor))\
        .filter(Recibo.data_recebido >= primeiro_dia_ano)\
        .scalar() or 0.0

    despesas_ano = db.session.query(db.func.sum(Despesa.valor))\
        .filter(Despesa.data >= primeiro_dia_ano)\
        .scalar() or 0.0

    # Petty cash
    levantamentos = db.session.query(db.func.sum(MovimentoCaixa.valor))\
        .filter(MovimentoCaixa.tipo == 'levantamento')\
        .scalar() or 0.0

    despesas_caixa = db.session.query(db.func.sum(MovimentoCaixa.valor))\
        .filter(MovimentoCaixa.tipo == 'despesa')\
        .scalar() or 0.0

    saldo_caixa = levantamentos - despesas_caixa

    # Count units with debt
    # (Simple version: units with no receipts at all this year)
    unidades_total = Unidade.query.filter_by(ativo=True).count()
    unidades_com_pagamento = db.session.query(Recibo.unidade_id)\
        .filter(Recibo.periodo_inicio >= primeiro_dia_ano)\
        .distinct().count()
    unidades_sem_pagamento = unidades_total - unidades_com_pagamento

    # Recent transactions
    recibos_recentes = Recibo.query.order_by(Recibo.criado_em.desc()).limit(5).all()
    despesas_recentes = Despesa.query.order_by(Despesa.criado_em.desc()).limit(5).all()

    # Combine and sort recent activity
    atividade = []
    for r in recibos_recentes:
        atividade.append({
            'tipo': 'receita',
            'data': r.criado_em,
            'texto': f'Recibo #{r.numero} — {r.unidade.codigo} pagou {format_currency(r.valor)}',
            'link': f'/receipts'
        })
    for d in despesas_recentes:
        atividade.append({
            'tipo': 'despesa',
            'data': d.criado_em,
            'texto': f'{d.categoria} — {d.descricao} ({format_currency(d.valor)})',
            'link': f'/expenses'
        })
    atividade.sort(key=lambda x: x['data'], reverse=True)
    atividade = atividade[:10]

    return render_template('dashboard/index.html',
                           saldo_banco=saldo_banco,
                           receitas_mes=receitas_mes,
                           despesas_mes=despesas_mes,
                           receitas_ano=receitas_ano,
                           despesas_ano=despesas_ano,
                           saldo_caixa=saldo_caixa,
                           unidades_sem_pagamento=unidades_sem_pagamento,
                           atividade=atividade,
                           format_currency=format_currency,
                           hoje=hoje)