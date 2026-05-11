from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.utils.decorators import admin_required
from app.utils.helpers import format_currency
from app.models import Configuracao
from app import db

settings_bp = Blueprint('settings', __name__)


@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    if request.method == 'POST':
        # Update all settings from form
        settings_keys = [
            'saldo_inicial_banco',
            'taxa_juros',
            'multa_incumprimento',
            'dias_tolerancia',
            'ultimo_numero_recibo',
            'iban',
        ]

        for chave in settings_keys:
            valor = request.form.get(chave)
            if valor is not None:
                config = Configuracao.query.filter_by(chave=chave).first()
                if config:
                    config.valor = valor
                else:
                    config = Configuracao(chave=chave, valor=valor)
                    db.session.add(config)

        db.session.commit()
        flash('Definições atualizadas com sucesso!', 'success')
        return redirect(url_for('settings.index'))

    # Load current settings
    configuracoes = {}
    all_configs = Configuracao.query.all()
    for config in all_configs:
        configuracoes[config.chave] = config.valor

    return render_template('settings/index.html', 
                           config=configuracoes,
                           format_currency=format_currency)