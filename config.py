#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuração da aplicação Flask
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class Config:
    """Configuração base"""
    
    # Configurações básicas do Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configurações do banco de dados
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Configurações JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Configurações de Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    # Configurações de Upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 4 * 1024 * 1024 * 1024))  # 4GB
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'txt,pdf,png,jpg,jpeg,gif').split(','))
    
    # Configurações de Paginação
    POSTS_PER_PAGE = int(os.getenv('POSTS_PER_PAGE', 10))
    USERS_PER_PAGE = int(os.getenv('USERS_PER_PAGE', 20))
    
    # Configurações da aplicação
    APP_NAME = os.getenv('APP_NAME', 'Flask Monolith Template')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    APP_HOST = os.getenv('APP_HOST', '127.0.0.1')
    APP_PORT = int(os.getenv('APP_PORT', 5000))
    
    # Configurações de segurança
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # Configurações de sessão
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Mudar para True em produção com HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configurações de CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    @staticmethod
    def init_app(app):
        """Inicializar configurações específicas da aplicação"""
        pass

class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    
    DEBUG = True
    TESTING = False
    
    # Configurações de desenvolvimento
    SQLALCHEMY_ECHO = True  # Log de queries SQL
    
    # Configurações de email para desenvolvimento (console)
    MAIL_SUPPRESS_SEND = False
    MAIL_DEBUG = True
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log para console em desenvolvimento
        import logging
        from logging import StreamHandler
        
        handler = StreamHandler()
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask Monolith startup')

class TestingConfig(Config):
    """Configuração para testes"""
    
    TESTING = True
    DEBUG = True
    
    # Banco de dados em memória para testes
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Desabilitar CSRF para testes
    WTF_CSRF_ENABLED = False
    
    # Configurações de email para testes
    MAIL_SUPPRESS_SEND = True
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

class ProductionConfig(Config):
    """Configuração para produção"""
    
    DEBUG = False
    TESTING = False
    
    # Configurações de segurança para produção
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_SSL_STRICT = True
    
    # Configurações de logging para produção
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log para arquivo em produção
        import logging
        from logging.handlers import RotatingFileHandler
        import os
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/flask_app.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask Monolith startup')

class DockerConfig(ProductionConfig):
    """Configuração para Docker"""
    
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        
        # Log para stdout no Docker
        import logging
        
        app.logger.handlers.clear()
        
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'
        ))
        
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)

# Mapeamento de configurações
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Obter configuração baseada no nome ou variável de ambiente"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    return config.get(config_name, config['default'])