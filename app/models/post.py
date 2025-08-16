#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo Post para gerenciamento de conteúdo
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db

class Post(db.Model):
    """Modelo de post/artigo"""
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    featured_image = db.Column(db.String(200))
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    views_count = db.Column(db.Integer, default=0, nullable=False)
    likes_count = db.Column(db.Integer, default=0, nullable=False)
    comments_count = db.Column(db.Integer, default=0, nullable=False)
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(300))
    tags = db.Column(db.String(500))  # Tags separadas por vírgula
    category = db.Column(db.String(100))
    reading_time = db.Column(db.Integer)  # Tempo de leitura em minutos
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    # Chave estrangeira
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, title, content, user_id, **kwargs):
        """Inicializar post"""
        self.title = title
        self.content = content
        self.user_id = user_id
        
        # Gerar slug automaticamente se não fornecido
        if 'slug' not in kwargs:
            self.slug = self.generate_slug(title)
        
        # Gerar excerpt automaticamente se não fornecido
        if 'excerpt' not in kwargs and content:
            self.excerpt = self.generate_excerpt(content)
        
        # Calcular tempo de leitura
        if 'reading_time' not in kwargs and content:
            self.reading_time = self.calculate_reading_time(content)
        
        # Definir campos opcionais
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    @staticmethod
    def generate_slug(title):
        """Gerar slug a partir do título"""
        import re
        import unicodedata
        
        # Normalizar unicode e remover acentos
        slug = unicodedata.normalize('NFKD', title)
        slug = slug.encode('ascii', 'ignore').decode('ascii')
        
        # Converter para minúsculas e substituir espaços por hífens
        slug = re.sub(r'[^\w\s-]', '', slug).strip().lower()
        slug = re.sub(r'[-\s]+', '-', slug)
        
        return slug
    
    @staticmethod
    def generate_excerpt(content, max_length=200):
        """Gerar excerpt a partir do conteúdo"""
        import re
        
        # Remover tags HTML
        clean_content = re.sub(r'<[^>]+>', '', content)
        
        # Truncar e adicionar reticências se necessário
        if len(clean_content) <= max_length:
            return clean_content
        
        excerpt = clean_content[:max_length].rsplit(' ', 1)[0]
        return f"{excerpt}..."
    
    @staticmethod
    def calculate_reading_time(content, words_per_minute=200):
        """Calcular tempo de leitura em minutos"""
        import re
        
        # Remover tags HTML e contar palavras
        clean_content = re.sub(r'<[^>]+>', '', content)
        word_count = len(clean_content.split())
        
        # Calcular tempo de leitura (mínimo 1 minuto)
        reading_time = max(1, round(word_count / words_per_minute))
        return reading_time
    
    def publish(self):
        """Publicar post"""
        self.is_published = True
        self.published_at = datetime.utcnow()
        db.session.commit()
    
    def unpublish(self):
        """Despublicar post"""
        self.is_published = False
        self.published_at = None
        db.session.commit()
    
    def increment_views(self):
        """Incrementar contador de visualizações"""
        self.views_count += 1
        db.session.commit()
    
    def increment_likes(self):
        """Incrementar contador de likes"""
        self.likes_count += 1
        db.session.commit()
    
    def get_tags_list(self):
        """Retornar lista de tags"""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def set_tags_list(self, tags_list):
        """Definir tags a partir de uma lista"""
        if isinstance(tags_list, list):
            self.tags = ', '.join(tags_list)
        else:
            self.tags = tags_list
    
    def get_url(self):
        """Retornar URL do post"""
        return f"/posts/{self.slug}"
    
    def to_dict(self, include_content=True):
        """Converter para dicionário"""
        data = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'excerpt': self.excerpt,
            'featured_image': self.featured_image,
            'is_published': self.is_published,
            'is_featured': self.is_featured,
            'views_count': self.views_count,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'meta_title': self.meta_title,
            'meta_description': self.meta_description,
            'tags': self.get_tags_list(),
            'category': self.category,
            'reading_time': self.reading_time,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'url': self.get_url(),
            'author': self.author.to_dict() if self.author else None
        }
        
        if include_content:
            data['content'] = self.content
            
        return data
    
    @staticmethod
    def get_published_posts(page=1, per_page=10):
        """Obter posts publicados com paginação"""
        return Post.query.filter_by(is_published=True).order_by(
            Post.published_at.desc()
        ).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    @staticmethod
    def get_featured_posts(limit=5):
        """Obter posts em destaque"""
        return Post.query.filter_by(
            is_published=True, is_featured=True
        ).order_by(
            Post.published_at.desc()
        ).limit(limit).all()
    
    @staticmethod
    def search_posts(query, page=1, per_page=10):
        """Buscar posts por título ou conteúdo"""
        return Post.query.filter(
            Post.is_published == True,
            db.or_(
                Post.title.contains(query),
                Post.content.contains(query),
                Post.tags.contains(query)
            )
        ).order_by(
            Post.published_at.desc()
        ).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    @staticmethod
    def find_by_slug(slug):
        """Encontrar post por slug"""
        return Post.query.filter_by(slug=slug, is_published=True).first()
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    def __str__(self):
        return self.title