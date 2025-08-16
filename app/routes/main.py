#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Routes principais da aplicação
"""

import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from app.models.post import Post
from app.models.user import User
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página inicial"""
    page = request.args.get('page', 1, type=int)
    per_page = int(os.getenv('POSTS_PER_PAGE', 10))
    
    # Obter posts publicados
    posts = Post.get_published_posts(page=page, per_page=per_page)
    
    # Obter posts em destaque
    featured_posts = Post.get_featured_posts(limit=3)
    
    return render_template('main/index.html', 
                         posts=posts, 
                         featured_posts=featured_posts)

@main_bp.route('/about')
def about():
    """Página sobre"""
    return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    """Página de contato"""
    return render_template('main/contact.html')

@main_bp.route('/posts')
def posts():
    """Lista de posts"""
    page = request.args.get('page', 1, type=int)
    per_page = int(os.getenv('POSTS_PER_PAGE', 10))
    category = request.args.get('category')
    tag = request.args.get('tag')
    
    query = Post.query.filter_by(is_published=True)
    
    # Filtrar por categoria
    if category:
        query = query.filter_by(category=category)
    
    # Filtrar por tag
    if tag:
        query = query.filter(Post.tags.contains(tag))
    
    posts = query.order_by(Post.published_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('main/posts.html', 
                         posts=posts, 
                         category=category, 
                         tag=tag)

@main_bp.route('/posts/<slug>')
def post_detail(slug):
    """Detalhes do post"""
    post = Post.find_by_slug(slug)
    
    if not post:
        flash('Post não encontrado.', 'error')
        return redirect(url_for('main.posts'))
    
    # Incrementar visualizações
    post.increment_views()
    
    # Obter posts relacionados (mesma categoria)
    related_posts = Post.query.filter(
        Post.is_published == True,
        Post.category == post.category,
        Post.id != post.id
    ).limit(3).all()
    
    return render_template('main/post_detail.html', 
                         post=post, 
                         related_posts=related_posts)

@main_bp.route('/search')
def search():
    """Busca de posts"""
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = int(os.getenv('POSTS_PER_PAGE', 10))
    
    if not query:
        flash('Digite um termo para buscar.', 'warning')
        return redirect(url_for('main.posts'))
    
    posts = Post.search_posts(query, page=page, per_page=per_page)
    
    return render_template('main/search_results.html', 
                         posts=posts, 
                         query=query)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard do usuário"""
    # Estatísticas do usuário
    user_posts = Post.query.filter_by(user_id=current_user.id)
    
    stats = {
        'total_posts': user_posts.count(),
        'published_posts': user_posts.filter_by(is_published=True).count(),
        'draft_posts': user_posts.filter_by(is_published=False).count(),
        'total_views': sum(post.views_count for post in user_posts),
        'total_likes': sum(post.likes_count for post in user_posts)
    }
    
    # Posts recentes do usuário
    recent_posts = user_posts.order_by(Post.created_at.desc()).limit(5).all()
    
    return render_template('main/dashboard.html', 
                         stats=stats, 
                         recent_posts=recent_posts)

@main_bp.route('/profile')
@login_required
def profile():
    """Perfil do usuário"""
    return render_template('main/profile.html', user=current_user)

@main_bp.route('/users/<username>')
def user_profile(username):
    """Perfil público do usuário"""
    user = User.find_by_username(username)
    
    if not user:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('main.index'))
    
    # Posts públicos do usuário
    page = request.args.get('page', 1, type=int)
    per_page = int(os.getenv('POSTS_PER_PAGE', 10))
    
    posts = Post.query.filter_by(
        user_id=user.id, 
        is_published=True
    ).order_by(
        Post.published_at.desc()
    ).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('main/user_profile.html', 
                         user=user, 
                         posts=posts)

@main_bp.route('/categories')
def categories():
    """Lista de categorias"""
    # Obter categorias únicas dos posts publicados
    categories = db.session.query(Post.category).filter(
        Post.is_published == True,
        Post.category.isnot(None)
    ).distinct().all()
    
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('main/categories.html', categories=categories)

@main_bp.route('/tags')
def tags():
    """Lista de tags"""
    # Obter todas as tags dos posts publicados
    posts_with_tags = Post.query.filter(
        Post.is_published == True,
        Post.tags.isnot(None)
    ).all()
    
    all_tags = []
    for post in posts_with_tags:
        all_tags.extend(post.get_tags_list())
    
    # Contar frequência das tags
    from collections import Counter
    tag_counts = Counter(all_tags)
    
    return render_template('main/tags.html', tag_counts=tag_counts)

@main_bp.route('/api/posts/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    """Curtir post (API)"""
    post = Post.query.get_or_404(post_id)
    post.increment_likes()
    
    return jsonify({
        'success': True,
        'likes_count': post.likes_count
    })

@main_bp.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'app_name': current_app.config.get('APP_NAME', 'Flask App'),
        'version': os.getenv('APP_VERSION', '1.0.0')
    })

# Context processor para variáveis globais
@main_bp.app_context_processor
def inject_global_vars():
    """Injetar variáveis globais nos templates"""
    return {
        'current_year': 2024,
        'site_name': os.getenv('APP_NAME', 'Flask Monolith'),
        'recent_posts': Post.query.filter_by(is_published=True).order_by(
            Post.published_at.desc()
        ).limit(5).all()
    }