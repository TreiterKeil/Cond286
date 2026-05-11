from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import admin_required
from app.utils.helpers import format_currency
from app.models import Unidade

units_bp = Blueprint('units', __name__)


@units_bp.route('/units')
@login_required
@admin_required
def list():
    unidades = Unidade.query.filter_by(ativo=True).order_by(Unidade.codigo).all()
    return render_template('units/list.html', unidades=unidades, format_currency=format_currency)


@units_bp.route('/units/<int:id>')
@login_required
@admin_required
def detail(id):
    unidade = Unidade.query.get_or_404(id)
    return render_template('units/detail.html', unidade=unidade, format_currency=format_currency)