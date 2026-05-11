from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Faça login para aceder a esta página.'
    login_manager.login_message_category = 'info'

    # Root redirect
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.is_admin():
                return redirect(url_for('dashboard.index'))
            else:
                return redirect(url_for('owner.my_unit'))
        return redirect(url_for('auth.login'))

    # Register blueprints
    from app.auth import auth_bp
    from app.dashboard import dashboard_bp
    from app.units import units_bp
    from app.receipts import receipts_bp
    from app.expenses import expenses_bp
    from app.map import map_bp
    from app.reconciliation import reconciliation_bp
    from app.petty_cash import petty_cash_bp
    from app.announcements import announcements_bp
    from app.settings import settings_bp
    from app.owner import owner_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(units_bp)
    app.register_blueprint(receipts_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(map_bp)
    app.register_blueprint(reconciliation_bp)
    app.register_blueprint(petty_cash_bp)
    app.register_blueprint(announcements_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(owner_bp)

    with app.app_context():
        db.create_all()

    return app