#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Monolith Template

Um template completo para aplicações Flask monolíticas com:
- Autenticação e autorização
- Sistema de posts/blog
- Painel administrativo
- API REST
- Interface moderna
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar extensões
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
cors = CORS()
jwt = JWTManager()

__version__ = '1.0.0'
__author__ = 'Flask Monolith Template'

def create_app(config_name=None):
    """Factory function para criar a aplicação Flask"""
    from config import get_config
    from cli import register_commands
    
    app = Flask(__name__)
    
    # Carregar configuração
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Inicializar configuração específica
    config_class.init_app(app)
    
    # Inicializar extensões com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    
    # Configurar Login Manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Registrar blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.api import api_bp
    from app.routes.admin import admin_bp
    from app.routes.admixture import admixture_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(admixture_bp, url_prefix='/admixture')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Context processors
    @app.context_processor
    def inject_config():
        return {
            'APP_NAME': app.config.get('APP_NAME', 'Flask App'),
            'APP_VERSION': app.config.get('APP_VERSION', '1.0.0')
        }
    
    # Registrar comandos CLI
    register_commands(app)
    
    return app

__all__ = ['create_app', 'db']