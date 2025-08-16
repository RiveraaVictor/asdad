#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Routes de administração
"""

import os
from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length
from app.models.user import User
from app.models.post import Post
from app import db

admin_bp = Blueprint('admin', __name__)

# Decorator para verificar se usuário é admin
def admin_required(f):
    """Decorator para verificar se usuário é administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Acesso negado. Apenas administradores podem acessar esta área.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# Formulários
class PostForm(FlaskForm):
    """Formulário para criar/editar posts"""
    title = StringField('Título', validators=[
        DataRequired(message='Título é obrigatório'),
        Length(min=5, max=200, message='Título deve ter entre 5 e 200 caracteres')
    ])
    content = TextAreaField('Conteúdo', validators=[
        DataRequired(message='Conteúdo é obrigatório')
    ])
    excerpt = TextAreaField('Resumo', validators=[
        Length(max=500, message='Resumo deve ter no máximo 500 caracteres')
    ])
    category = StringField('Categoria', validators=[
        Length(max=100, message='Categoria deve ter no máximo 100 caracteres')
    ])
    tags = StringField('Tags (separadas por vírgula)', validators=[
        Length(max=500, message='Tags devem ter no máximo 500 caracteres')
    ])
    meta_title = StringField('Meta Título (SEO)', validators=[
        Length(max=200, message='Meta título deve ter no máximo 200 caracteres')
    ])
    meta_description = TextAreaField('Meta Descrição (SEO)', validators=[
        Length(max=300, message='Meta descrição deve ter no máximo 300 caracteres')
    ])
    is_published = BooleanField('Publicado')
    is_featured = BooleanField('Em Destaque')

class UserForm(FlaskForm):
    """Formulário para editar usuários"""
    first_name = StringField('Nome', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=2, max=50, message='Nome deve ter entre 2 e 50 caracteres')
    ])
    last_name = StringField('Sobrenome', validators=[
        DataRequired(message='Sobrenome é obrigatório'),
        Length(min=2, max=50, message='Sobrenome deve ter entre 2 e 50 caracteres')
    ])
    bio = TextAreaField('Bio', validators=[
        Length(max=500, message='Bio deve ter no máximo 500 caracteres')
    ])
    location = StringField('Localização', validators=[
        Length(max=100, message='Localização deve ter no máximo 100 caracteres')
    ])
    website = StringField('Website', validators=[
        Length(max=200, message='Website deve ter no máximo 200 caracteres')
    ])
    is_active = BooleanField('Ativo')
    is_admin = BooleanField('Administrador')
    email_confirmed = BooleanField('Email Confirmado')

# Dashboard Admin
@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """Dashboard administrativo"""
    # Estatísticas gerais
    stats = {
        'total_users': User.query.count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        'admin_users': User.query.filter_by(is_admin=True).count(),
        'total_posts': Post.query.count(),
        'published_posts': Post.query.filter_by(is_published=True).count(),
        'draft_posts': Post.query.filter_by(is_published=False).count(),
        'featured_posts': Post.query.filter_by(is_featured=True).count(),
        'total_views': sum(post.views_count for post in Post.query.all()),
        'total_likes': sum(post.likes_count for post in Post.query.all())
    }
    
    # Posts recentes
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    
    # Usuários recentes
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_posts=recent_posts, 
                         recent_users=recent_users)

# Gerenciamento de Posts
@admin_bp.route('/posts')
@login_required
@admin_required
def posts():
    """Lista de posts para administração"""
    page = request.args.get('page', 1, type=int)
    per_page = int(os.getenv('POSTS_PER_PAGE', 20))
    status = request.args.get('status', 'all')
    search = request.args.get('search', '')
    
    query = Post.query
    
    # Filtrar por status
    if status == 'published':
        query = query.filter_by(is_published=True)
    elif status == 'draft':
        query = query.filter_by(is_published=False)
    elif status == 'featured':
        query = query.filter_by(is_featured=True)
    
    # Buscar por título
    if search:
        query = query.filter(Post.title.contains(search))
    
    posts = query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/posts.html', 
                         posts=posts, 
                         status=status, 
                         search=search)

@admin_bp.route('/posts/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_post():
    """Criar novo post"""
    form = PostForm()
    
    if form.validate_on_submit():
        try:
            post = Post(
                title=form.title.data,
                content=form.content.data,
                user_id=current_user.id,
                excerpt=form.excerpt.data,
                category=form.category.data,
                tags=form.tags.data,
                meta_title=form.meta_title.data,
                meta_description=form.meta_description.data,
                is_published=form.is_published.data,
                is_featured=form.is_featured.data
            )
            
            if post.is_published:
                post.publish()
            
            db.session.add(post)
            db.session.commit()
            
            flash('Post criado com sucesso!', 'success')
            return redirect(url_for('admin.posts'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar post. Tente novamente.', 'error')
    
    return render_template('admin/post_form.html', form=form, action='Criar')

@admin_bp.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_post(post_id):
    """Editar post"""
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    
    # Converter tags para string
    if post.tags:
        form.tags.data = post.tags
    
    if form.validate_on_submit():
        try:
            was_published = post.is_published
            
            post.title = form.title.data
            post.content = form.content.data
            post.excerpt = form.excerpt.data or Post.generate_excerpt(form.content.data)
            post.category = form.category.data
            post.tags = form.tags.data
            post.meta_title = form.meta_title.data
            post.meta_description = form.meta_description.data
            post.is_published = form.is_published.data
            post.is_featured = form.is_featured.data
            
            # Atualizar slug se título mudou
            post.slug = Post.generate_slug(form.title.data)
            
            # Atualizar tempo de leitura
            post.reading_time = Post.calculate_reading_time(form.content.data)
            
            # Gerenciar publicação
            if not was_published and post.is_published:
                post.publish()
            elif was_published and not post.is_published:
                post.unpublish()
            
            db.session.commit()
            
            flash('Post atualizado com sucesso!', 'success')
            return redirect(url_for('admin.posts'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar post. Tente novamente.', 'error')
    
    return render_template('admin/post_form.html', 
                         form=form, 
                         post=post, 
                         action='Editar')

@admin_bp.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_post(post_id):
    """Deletar post"""
    post = Post.query.get_or_404(post_id)
    
    try:
        title = post.title
        db.session.delete(post)
        db.session.commit()
        
        flash(f'Post "{title}" deletado com sucesso!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('Erro ao deletar post. Tente novamente.', 'error')
    
    return redirect(url_for('admin.posts'))

# Gerenciamento de Usuários
@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """Lista de usuários para administração"""
    page = request.args.get('page', 1, type=int)
    per_page = int(os.getenv('USERS_PER_PAGE', 20))
    status = request.args.get('status', 'all')
    search = request.args.get('search', '')
    
    query = User.query
    
    # Filtrar por status
    if status == 'active':
        query = query.filter_by(is_active=True)
    elif status == 'inactive':
        query = query.filter_by(is_active=False)
    elif status == 'admin':
        query = query.filter_by(is_admin=True)
    
    # Buscar por nome ou username
    if search:
        query = query.filter(
            db.or_(
                User.username.contains(search),
                User.first_name.contains(search),
                User.last_name.contains(search),
                User.email.contains(search)
            )
        )
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/users.html', 
                         users=users, 
                         status=status, 
                         search=search)

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Editar usuário"""
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        try:
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.bio = form.bio.data
            user.location = form.location.data
            user.website = form.website.data
            user.is_active = form.is_active.data
            user.email_confirmed = form.email_confirmed.data
            
            # Apenas super admin pode alterar status de admin
            if current_user.id == 1:  # Assumindo que ID 1 é super admin
                user.is_admin = form.is_admin.data
            
            db.session.commit()
            
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('admin.users'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar usuário. Tente novamente.', 'error')
    
    return render_template('admin/user_form.html', 
                         form=form, 
                         user=user)

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    """Ativar/desativar usuário"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('Você não pode desativar sua própria conta.', 'error')
        return redirect(url_for('admin.users'))
    
    try:
        user.is_active = not user.is_active
        db.session.commit()
        
        status = 'ativado' if user.is_active else 'desativado'
        flash(f'Usuário {user.username} {status} com sucesso!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('Erro ao alterar status do usuário.', 'error')
    
    return redirect(url_for('admin.users'))

# API Endpoints para Admin
@admin_bp.route('/api/stats')
@login_required
@admin_required
def api_admin_stats():
    """Estatísticas para dashboard admin"""
    stats = {
        'users': {
            'total': User.query.count(),
            'active': User.query.filter_by(is_active=True).count(),
            'inactive': User.query.filter_by(is_active=False).count(),
            'admin': User.query.filter_by(is_admin=True).count()
        },
        'posts': {
            'total': Post.query.count(),
            'published': Post.query.filter_by(is_published=True).count(),
            'draft': Post.query.filter_by(is_published=False).count(),
            'featured': Post.query.filter_by(is_featured=True).count()
        },
        'engagement': {
            'total_views': sum(post.views_count for post in Post.query.all()),
            'total_likes': sum(post.likes_count for post in Post.query.all()),
            'avg_views_per_post': 0,
            'avg_likes_per_post': 0
        }
    }
    
    # Calcular médias
    if stats['posts']['published'] > 0:
        published_posts = Post.query.filter_by(is_published=True).all()
        stats['engagement']['avg_views_per_post'] = round(
            sum(post.views_count for post in published_posts) / len(published_posts), 2
        )
        stats['engagement']['avg_likes_per_post'] = round(
            sum(post.likes_count for post in published_posts) / len(published_posts), 2
        )
    
    return jsonify(stats)

# Context processor para admin
@admin_bp.app_context_processor
def inject_admin_vars():
    """Injetar variáveis para templates admin"""
    if current_user.is_authenticated and current_user.is_admin:
        return {
            'pending_posts': Post.query.filter_by(is_published=False).count(),
            'inactive_users': User.query.filter_by(is_active=False).count()
        }
    return {}