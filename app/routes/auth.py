#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Routes de autenticação
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

# Formulários WTF
class LoginForm(FlaskForm):
    """Formulário de login"""
    username = StringField('Username ou Email', validators=[
        DataRequired(message='Username ou email é obrigatório')
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória')
    ])
    remember_me = BooleanField('Lembrar de mim')

class RegisterForm(FlaskForm):
    """Formulário de registro"""
    username = StringField('Username', validators=[
        DataRequired(message='Username é obrigatório'),
        Length(min=3, max=20, message='Username deve ter entre 3 e 20 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    first_name = StringField('Nome', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=2, max=50, message='Nome deve ter entre 2 e 50 caracteres')
    ])
    last_name = StringField('Sobrenome', validators=[
        DataRequired(message='Sobrenome é obrigatório'),
        Length(min=2, max=50, message='Sobrenome deve ter entre 2 e 50 caracteres')
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória'),
        Length(min=6, message='Senha deve ter pelo menos 6 caracteres')
    ])
    password_confirm = PasswordField('Confirmar Senha', validators=[
        DataRequired(message='Confirmação de senha é obrigatória'),
        EqualTo('password', message='Senhas não coincidem')
    ])
    
    def validate_username(self, username):
        """Validar se username já existe"""
        user = User.find_by_username(username.data)
        if user:
            raise ValidationError('Username já está em uso. Escolha outro.')
    
    def validate_email(self, email):
        """Validar se email já existe"""
        user = User.find_by_email(email.data)
        if user:
            raise ValidationError('Email já está em uso. Escolha outro.')

class ProfileForm(FlaskForm):
    """Formulário de perfil"""
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

class ChangePasswordForm(FlaskForm):
    """Formulário para alterar senha"""
    current_password = PasswordField('Senha Atual', validators=[
        DataRequired(message='Senha atual é obrigatória')
    ])
    new_password = PasswordField('Nova Senha', validators=[
        DataRequired(message='Nova senha é obrigatória'),
        Length(min=6, message='Nova senha deve ter pelo menos 6 caracteres')
    ])
    new_password_confirm = PasswordField('Confirmar Nova Senha', validators=[
        DataRequired(message='Confirmação de nova senha é obrigatória'),
        EqualTo('new_password', message='Senhas não coincidem')
    ])
    
    def validate_current_password(self, current_password):
        """Validar senha atual"""
        if not current_user.check_password(current_password.data):
            raise ValidationError('Senha atual incorreta.')

# Routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login do usuário"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username_or_email = form.username.data
        password = form.password.data
        remember = form.remember_me.data
        
        # Tentar encontrar usuário por username ou email
        user = User.find_by_username(username_or_email)
        if not user:
            user = User.find_by_email(username_or_email)
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Sua conta está desativada. Entre em contato com o administrador.', 'error')
                return render_template('auth/login.html', form=form)
            
            login_user(user, remember=remember)
            user.update_last_login()
            
            flash(f'Bem-vindo, {user.get_full_name()}!', 'success')
            
            # Redirecionar para página solicitada ou dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Username/email ou senha incorretos.', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de novo usuário"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        try:
            user = User.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            
            flash('Conta criada com sucesso! Você pode fazer login agora.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar conta. Tente novamente.', 'error')
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    flash('Você foi desconectado com sucesso.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Editar perfil do usuário"""
    form = ProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        try:
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.bio = form.bio.data
            current_user.location = form.location.data
            current_user.website = form.website.data
            
            db.session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('auth.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar perfil. Tente novamente.', 'error')
    
    return render_template('auth/profile.html', form=form)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Alterar senha do usuário"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        try:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            
            flash('Senha alterada com sucesso!', 'success')
            return redirect(url_for('auth.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao alterar senha. Tente novamente.', 'error')
    
    return render_template('auth/change_password.html', form=form)

@auth_bp.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    """Deletar conta do usuário"""
    password = request.form.get('password')
    
    if not password or not current_user.check_password(password):
        flash('Senha incorreta.', 'error')
        return redirect(url_for('auth.profile'))
    
    try:
        # Deletar posts do usuário
        for post in current_user.posts:
            db.session.delete(post)
        
        # Deletar usuário
        user_name = current_user.get_full_name()
        db.session.delete(current_user)
        db.session.commit()
        
        logout_user()
        flash(f'Conta de {user_name} foi deletada com sucesso.', 'info')
        return redirect(url_for('main.index'))
        
    except Exception as e:
        db.session.rollback()
        flash('Erro ao deletar conta. Tente novamente.', 'error')
        return redirect(url_for('auth.profile'))

# Context processor para formulários
@auth_bp.app_context_processor
def inject_auth_forms():
    """Injetar formulários de autenticação nos templates"""
    return {
        'login_form': LoginForm() if not current_user.is_authenticated else None
    }