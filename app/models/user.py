#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo User para autenticação e gerenciamento de usuários
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """Modelo de usuário com autenticação"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    avatar_url = db.Column(db.String(200))
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    website = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relacionamentos
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, username, email, password, first_name, last_name, **kwargs):
        """Inicializar usuário com senha hash"""
        self.username = username
        self.email = email
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        
        # Definir campos opcionais
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def set_password(self, password):
        """Definir senha com hash"""
        self.password_hash = generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verificar senha"""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Retornar nome completo"""
        return f"{self.first_name} {self.last_name}"
    
    def get_initials(self):
        """Retornar iniciais do nome"""
        return f"{self.first_name[0]}{self.last_name[0]}".upper()
    
    def is_authenticated(self):
        """Verificar se usuário está autenticado"""
        return True
    
    def is_anonymous(self):
        """Verificar se usuário é anônimo"""
        return False
    
    def get_id(self):
        """Retornar ID do usuário como string"""
        return str(self.id)
    
    def update_last_login(self):
        """Atualizar último login"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self, include_email=False):
        """Converter para dicionário"""
        data = {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'initials': self.get_initials(),
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'email_confirmed': self.email_confirmed,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            'location': self.location,
            'website': self.website,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'posts_count': self.posts.count()
        }
        
        if include_email:
            data['email'] = self.email
            
        return data
    
    @staticmethod
    def find_by_username(username):
        """Encontrar usuário por username"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def find_by_email(email):
        """Encontrar usuário por email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def create_user(username, email, password, first_name, last_name, **kwargs):
        """Criar novo usuário"""
        user = User(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **kwargs
        )
        
        db.session.add(user)
        db.session.commit()
        return user
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def __str__(self):
        return self.get_full_name()