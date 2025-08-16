#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API REST endpoints
"""

import os
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    create_refresh_token, get_jwt
)
from app.models.user import User
from app.models.post import Post
from app import db

api_bp = Blueprint('api', __name__)

# Blacklist para tokens JWT revogados
blacklisted_tokens = set()

# Helpers
def success_response(data=None, message="Success", status_code=200):
    """Resposta de sucesso padronizada"""
    response = {
        'success': True,
        'message': message,
        'data': data
    }
    return jsonify(response), status_code

def error_response(message="Error", status_code=400, errors=None):
    """Resposta de erro padronizada"""
    response = {
        'success': False,
        'message': message,
        'errors': errors
    }
    return jsonify(response), status_code

def validate_json_data(required_fields):
    """Validar dados JSON obrigatórios"""
    if not request.is_json:
        return error_response("Content-Type deve ser application/json", 400)
    
    data = request.get_json()
    if not data:
        return error_response("Dados JSON são obrigatórios", 400)
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return error_response(
            f"Campos obrigatórios ausentes: {', '.join(missing_fields)}", 
            400
        )
    
    return None

# JWT Token Blacklist
@api_bp.before_app_request
def check_if_token_revoked():
    """Verificar se token JWT foi revogado"""
    pass

# Authentication Endpoints
@api_bp.route('/auth/login', methods=['POST'])
def api_login():
    """Login via API"""
    validation_error = validate_json_data(['username', 'password'])
    if validation_error:
        return validation_error
    
    data = request.get_json()
    username_or_email = data['username']
    password = data['password']
    
    # Encontrar usuário
    user = User.find_by_username(username_or_email)
    if not user:
        user = User.find_by_email(username_or_email)
    
    if not user or not user.check_password(password):
        return error_response("Credenciais inválidas", 401)
    
    if not user.is_active:
        return error_response("Conta desativada", 403)
    
    # Criar tokens
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
    )
    refresh_token = create_refresh_token(identity=user.id)
    
    # Atualizar último login
    user.update_last_login()
    
    return success_response({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict(include_email=True)
    }, "Login realizado com sucesso")

@api_bp.route('/auth/register', methods=['POST'])
def api_register():
    """Registro via API"""
    validation_error = validate_json_data([
        'username', 'email', 'password', 'first_name', 'last_name'
    ])
    if validation_error:
        return validation_error
    
    data = request.get_json()
    
    # Verificar se usuário já existe
    if User.find_by_username(data['username']):
        return error_response("Username já está em uso", 409)
    
    if User.find_by_email(data['email']):
        return error_response("Email já está em uso", 409)
    
    try:
        user = User.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            bio=data.get('bio', ''),
            location=data.get('location', ''),
            website=data.get('website', '')
        )
        
        return success_response(
            user.to_dict(include_email=True),
            "Usuário criado com sucesso",
            201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response("Erro ao criar usuário", 500)

@api_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def api_refresh():
    """Renovar token de acesso"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_active:
        return error_response("Usuário inválido", 401)
    
    new_access_token = create_access_token(
        identity=current_user_id,
        expires_delta=timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
    )
    
    return success_response({
        'access_token': new_access_token
    }, "Token renovado com sucesso")

@api_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def api_logout():
    """Logout via API"""
    jti = get_jwt()['jti']
    blacklisted_tokens.add(jti)
    
    return success_response(message="Logout realizado com sucesso")

@api_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def api_me():
    """Obter dados do usuário atual"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return error_response("Usuário não encontrado", 404)
    
    return success_response(user.to_dict(include_email=True))

# Posts Endpoints
@api_bp.route('/posts', methods=['GET'])
def api_posts():
    """Listar posts"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    category = request.args.get('category')
    tag = request.args.get('tag')
    search = request.args.get('search')
    
    query = Post.query.filter_by(is_published=True)
    
    # Filtros
    if category:
        query = query.filter_by(category=category)
    
    if tag:
        query = query.filter(Post.tags.contains(tag))
    
    if search:
        query = query.filter(
            db.or_(
                Post.title.contains(search),
                Post.content.contains(search)
            )
        )
    
    posts = query.order_by(Post.published_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return success_response({
        'posts': [post.to_dict(include_content=False) for post in posts.items],
        'pagination': {
            'page': posts.page,
            'pages': posts.pages,
            'per_page': posts.per_page,
            'total': posts.total,
            'has_next': posts.has_next,
            'has_prev': posts.has_prev
        }
    })

@api_bp.route('/posts/<slug>', methods=['GET'])
def api_post_detail(slug):
    """Obter detalhes do post"""
    post = Post.find_by_slug(slug)
    
    if not post:
        return error_response("Post não encontrado", 404)
    
    # Incrementar visualizações
    post.increment_views()
    
    return success_response(post.to_dict())

@api_bp.route('/posts', methods=['POST'])
@jwt_required()
def api_create_post():
    """Criar novo post"""
    validation_error = validate_json_data(['title', 'content'])
    if validation_error:
        return validation_error
    
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    try:
        post = Post(
            title=data['title'],
            content=data['content'],
            user_id=current_user_id,
            excerpt=data.get('excerpt'),
            category=data.get('category'),
            tags=data.get('tags'),
            is_published=data.get('is_published', False),
            is_featured=data.get('is_featured', False),
            meta_title=data.get('meta_title'),
            meta_description=data.get('meta_description')
        )
        
        if post.is_published:
            post.published_at = datetime.utcnow()
        
        db.session.add(post)
        db.session.commit()
        
        return success_response(
            post.to_dict(),
            "Post criado com sucesso",
            201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response("Erro ao criar post", 500)

@api_bp.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def api_update_post(post_id):
    """Atualizar post"""
    current_user_id = get_jwt_identity()
    post = Post.query.get(post_id)
    
    if not post:
        return error_response("Post não encontrado", 404)
    
    if post.user_id != current_user_id:
        return error_response("Sem permissão para editar este post", 403)
    
    if not request.is_json:
        return error_response("Content-Type deve ser application/json", 400)
    
    data = request.get_json()
    
    try:
        # Atualizar campos
        if 'title' in data:
            post.title = data['title']
            post.slug = Post.generate_slug(data['title'])
        
        if 'content' in data:
            post.content = data['content']
            post.excerpt = Post.generate_excerpt(data['content'])
            post.reading_time = Post.calculate_reading_time(data['content'])
        
        if 'category' in data:
            post.category = data['category']
        
        if 'tags' in data:
            post.tags = data['tags']
        
        if 'is_published' in data:
            was_published = post.is_published
            post.is_published = data['is_published']
            
            if not was_published and post.is_published:
                post.published_at = datetime.utcnow()
            elif was_published and not post.is_published:
                post.published_at = None
        
        if 'is_featured' in data:
            post.is_featured = data['is_featured']
        
        if 'meta_title' in data:
            post.meta_title = data['meta_title']
        
        if 'meta_description' in data:
            post.meta_description = data['meta_description']
        
        post.updated_at = datetime.utcnow()
        db.session.commit()
        
        return success_response(
            post.to_dict(),
            "Post atualizado com sucesso"
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response("Erro ao atualizar post", 500)

@api_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def api_delete_post(post_id):
    """Deletar post"""
    current_user_id = get_jwt_identity()
    post = Post.query.get(post_id)
    
    if not post:
        return error_response("Post não encontrado", 404)
    
    if post.user_id != current_user_id:
        return error_response("Sem permissão para deletar este post", 403)
    
    try:
        db.session.delete(post)
        db.session.commit()
        
        return success_response(message="Post deletado com sucesso")
        
    except Exception as e:
        db.session.rollback()
        return error_response("Erro ao deletar post", 500)

@api_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def api_like_post(post_id):
    """Curtir post"""
    post = Post.query.get(post_id)
    
    if not post:
        return error_response("Post não encontrado", 404)
    
    post.increment_likes()
    
    return success_response({
        'likes_count': post.likes_count
    }, "Post curtido com sucesso")

# Users Endpoints
@api_bp.route('/users/<username>', methods=['GET'])
def api_user_profile(username):
    """Obter perfil público do usuário"""
    user = User.find_by_username(username)
    
    if not user:
        return error_response("Usuário não encontrado", 404)
    
    return success_response(user.to_dict())

# Statistics Endpoints
@api_bp.route('/stats', methods=['GET'])
def api_stats():
    """Estatísticas gerais da aplicação"""
    stats = {
        'total_users': User.query.count(),
        'total_posts': Post.query.filter_by(is_published=True).count(),
        'total_views': sum(post.views_count for post in Post.query.all()),
        'total_likes': sum(post.likes_count for post in Post.query.all())
    }
    
    return success_response(stats)

# Error Handlers
@api_bp.errorhandler(404)
def api_not_found(error):
    return error_response("Endpoint não encontrado", 404)

@api_bp.errorhandler(405)
def api_method_not_allowed(error):
    return error_response("Método não permitido", 405)

@api_bp.errorhandler(500)
def api_internal_error(error):
    db.session.rollback()
    return error_response("Erro interno do servidor", 500)