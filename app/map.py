from flask import Blueprint, render_template
from flask_login import login_required
from datetime import date
from dateutil.relativedelta import relativedelta
from app.utils.decorators import admin_required
from app.utils.helpers import format_currency
from app.models import Unidade, Recibo, Configuracao
from app import db

map_bp = Blueprint('map', __name__)


@map_bp.route('/map')
@login_required
@admin_required
def index():
    unidades = Unidade.query.filter_by(ativo=True).order_by(Unidade.codigo).all()
    
    # Define the periods we want to track
    hoje = date.today()
    ano_atual = hoje.year
    
    periodos = [
        {
            'nome': f'Jan a Jun {ano_atual - 1}',
            'inicio': date(ano_atual - 1, 1, 1),
            'fim': date(ano_atual - 1, 6, 30),
            'valor_esperado': 90.00
        },
        {
            'nome': f'Jul a Dez {ano_atual - 1}',
            'inicio': date(ano_atual - 1, 7, 1),
            'fim': date(ano_atual - 1, 12, 31),
            'valor_esperado': 90.00
        },
        {
            'nome': f'Jan a Jun {ano_atual}',
            'inicio': date(ano_atual, 1, 1),
            'fim': date(ano_atual, 6, 30),
            'valor_esperado': 90.00
        },
        {
            'nome': f'Jul a Dez {ano_atual}',
            'inicio': date(ano_atual, 7, 1),
            'fim': date(ano_atual, 12, 31),
            'valor_esperado': 90.00
        },
    ]
    
    # Build payment status matrix
    mapa = []
    for unidade in unidades:
        linha = {
            'unidade': unidade,
            'periodos': []
        }
        
        for periodo in periodos:
            # Sum all receipts that fall within this period
            total_pago = db.session.query(db.func.sum(Recibo.valor))\
                .filter(
                    Recibo.unidade_id == unidade.id,
                    Recibo.periodo_inicio >= periodo['inicio'],
                    Recibo.periodo_fim <= periodo['fim']
                ).scalar() or 0.0
            
            valor_esperado = periodo['valor_esperado']
            
            if total_pago >= valor_esperado:
                status = 'pago'
            elif total_pago > 0:
                status = 'parcial'
            elif periodo['fim'] < hoje:
                status = 'atraso'
            else:
                status = 'pendente'
            
            linha['periodos'].append({
                'status': status,
                'total_pago': total_pago,
                'valor_esperado': valor_esperado,
                'recibos': Recibo.query.filter(
                    Recibo.unidade_id == unidade.id,
                    Recibo.periodo_inicio >= periodo['inicio'],
                    Recibo.periodo_fim <= periodo['fim']
                ).all()
            })
        
        mapa.append(linha)
    
    return render_template('map/index.html', 
                           mapa=mapa, 
                           periodos=periodos,
                           format_currency=format_currency,
                           hoje=hoje)