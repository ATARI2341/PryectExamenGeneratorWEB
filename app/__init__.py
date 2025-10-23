# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    from .models import Usuario
    return db.session.get(Usuario, int(user_id))


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecreto'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/ExamenGeneratorWEB.db'

    db.init_app(app)
    login_manager.init_app(app)

    # Registramos los Blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/') 

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/') 

    with app.app_context():
        db.create_all()

    return app