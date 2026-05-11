from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.utils.helpers import format_currency
from app.models import Configuracao

owner_bp = Blueprint('owner', __name__)


@owner_bp.route('/my-unit')
@login_required
def my_unit():
    unidade = current_user.unidade
    
    # Get bank balance from settings
    config_saldo = Configuracao.query.filter_by(chave='saldo_inicial_banco').first()
    saldo_banco = float(config_saldo.valor) if config_saldo else 2995.83
    
    return render_template('owner/my_unit.html', 
                           unidade=unidade, 
                           saldo_banco=saldo_banco,
                           format_currency=format_currency)