from datetime import datetime, date
from dateutil.relativedelta import relativedelta


def format_currency(valor):
    """Formata valor como € X.XXX,XX"""
    if valor is None:
        return '€ 0,00'
    return f"€ {valor:,.2f}".replace(',', ' ').replace('.', ',').replace(' ', '.')


def mes_por_extenso(mes):
    """Retorna o nome do mês em português"""
    meses = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    return meses.get(mes, '')


def periodo_formatado(inicio, fim):
    """Formata período como 'Jan a Jun 2026'"""
    if isinstance(inicio, date) and isinstance(fim, date):
        return f"{mes_por_extenso(inicio.month)[:3]} a {mes_por_extenso(fim.month)[:3]} {fim.year}"
    return ''


def calcular_juros(valor_em_divida, data_vencimento, taxa_anual=10.0):
    """Calcula juros de mora sobre valor em dívida"""
    if valor_em_divida <= 0:
        return 0.0
    dias_atraso = (date.today() - data_vencimento).days
    if dias_atraso <= 0:
        return 0.0
    return round(valor_em_divida * (taxa_anual / 100) * (dias_atraso / 365), 2)


def gerar_numero_recibo():
    """Gera próximo número de recibo sequencial"""
    from app.models import Recibo, Configuracao
    config = Configuracao.query.filter_by(chave='ultimo_numero_recibo').first()
    if config:
        numero = int(config.valor) + 1
        config.valor = str(numero)
        from app import db
        db.session.commit()
        return numero
    # Default start at 896 if no config
    novo = Configuracao(chave='ultimo_numero_recibo', valor='896')
    from app import db
    db.session.add(novo)
    db.session.commit()
    return 896