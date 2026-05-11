from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    funcao = db.Column(db.String(20), nullable=False, default='owner')  # 'admin' or 'owner'
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidades.id'), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    unidade = db.relationship('Unidade', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.funcao == 'admin'

    def __repr__(self):
        return f'<User {self.nome}>'


class Unidade(db.Model):
    __tablename__ = 'unidades'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    piso = db.Column(db.String(10))
    posicao = db.Column(db.String(10))
    quota_mensal = db.Column(db.Float, default=15.00)
    nome_proprietario = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Unidade {self.codigo}>'

    @property
    def quota_anual(self):
        return self.quota_mensal * 12

    @property
    def quota_semestral(self):
        return self.quota_mensal * 6

    @property
    def quota_bimestral(self):
        return self.quota_mensal * 2


class Recibo(db.Model):
    __tablename__ = 'recibos'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidades.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    periodo_inicio = db.Column(db.Date, nullable=False)
    periodo_fim = db.Column(db.Date, nullable=False)
    metodo_pagamento = db.Column(db.String(30))
    data_recebido = db.Column(db.Date, nullable=False)
    notas = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    unidade = db.relationship('Unidade', backref='recibos')


class Despesa(db.Model):
    __tablename__ = 'despesas'

    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(300), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False)
    metodo_pagamento = db.Column(db.String(30))
    pago_por = db.Column(db.String(200))
    reembolsado = db.Column(db.Boolean, default=False)
    data_reembolso = db.Column(db.Date, nullable=True)
    comprovativo_path = db.Column(db.String(300))
    notas = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)


class MovimentoCaixa(db.Model):
    __tablename__ = 'movimentos_caixa'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(300))
    data = db.Column(db.Date, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)


class MovimentoBanco(db.Model):
    __tablename__ = 'movimentos_banco'

    id = db.Column(db.Integer, primary_key=True)
    data_movimento = db.Column(db.Date, nullable=False)
    data_valor = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.String(300))
    montante = db.Column(db.Float, nullable=False)
    saldo_apos = db.Column(db.Float)
    reconciliado = db.Column(db.Boolean, default=False)
    recibo_id = db.Column(db.Integer, db.ForeignKey('recibos.id'), nullable=True)
    despesa_id = db.Column(db.Integer, db.ForeignKey('despesas.id'), nullable=True)

    recibo = db.relationship('Recibo', backref='movimentos_banco')
    despesa = db.relationship('Despesa', backref='movimentos_banco')


class Anuncio(db.Model):
    __tablename__ = 'anuncios'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    conteudo = db.Column(db.Text)
    anexo_path = db.Column(db.String(300))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)


class Configuracao(db.Model):
    __tablename__ = 'configuracoes'

    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.String(300))