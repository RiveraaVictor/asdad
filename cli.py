#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comandos CLI para gerenciamento da aplicação
"""

import os
import click
from flask import current_app
from flask.cli import with_appcontext
from app import db
from app.models.user import User
from app.models.post import Post
from datetime import datetime

@click.command()
@with_appcontext
def init_db():
    """Inicializar banco de dados"""
    click.echo('Inicializando banco de dados...')
    
    # Criar todas as tabelas
    db.create_all()
    
    click.echo('Banco de dados inicializado com sucesso!')

@click.command()
@with_appcontext
def reset_db():
    """Resetar banco de dados (CUIDADO: apaga todos os dados)"""
    if click.confirm('Tem certeza que deseja resetar o banco de dados? Todos os dados serão perdidos.'):
        click.echo('Resetando banco de dados...')
        
        # Dropar todas as tabelas
        db.drop_all()
        
        # Recriar todas as tabelas
        db.create_all()
        
        click.echo('Banco de dados resetado com sucesso!')
    else:
        click.echo('Operação cancelada.')

@click.command()
@with_appcontext
def create_admin():
    """Criar usuário administrador"""
    click.echo('Criando usuário administrador...')
    
    # Verificar se já existe um admin
    admin = User.query.filter_by(is_admin=True).first()
    if admin:
        click.echo(f'Já existe um administrador: {admin.username}')
        if not click.confirm('Deseja criar outro administrador?'):
            return
    
    # Coletar dados do administrador
    username = click.prompt('Username', type=str)
    email = click.prompt('Email', type=str)
    first_name = click.prompt('Nome', type=str)
    last_name = click.prompt('Sobrenome', type=str)
    password = click.prompt('Senha', type=str, hide_input=True, confirmation_prompt=True)
    
    # Verificar se username ou email já existem
    if User.find_by_username(username):
        click.echo(f'Erro: Username "{username}" já está em uso.')
        return
    
    if User.find_by_email(email):
        click.echo(f'Erro: Email "{email}" já está em uso.')
        return
    
    try:
        # Criar usuário administrador
        admin = User.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_admin=True,
            is_active=True,
            email_confirmed=True
        )
        
        click.echo(f'Administrador "{username}" criado com sucesso!')
        click.echo(f'ID: {admin.id}')
        click.echo(f'Email: {admin.email}')
        
    except Exception as e:
        click.echo(f'Erro ao criar administrador: {str(e)}')
        db.session.rollback()

@click.command()
@with_appcontext
def seed_data():
    """Inserir dados de exemplo"""
    click.echo('Inserindo dados de exemplo...')
    
    try:
        # Criar usuário de exemplo se não existir
        demo_user = User.find_by_username('demo')
        if not demo_user:
            demo_user = User.create_user(
                username='demo',
                email='demo@example.com',
                password='demo123',
                first_name='Demo',
                last_name='User',
                bio='Usuário de demonstração do sistema',
                is_active=True,
                email_confirmed=True
            )
            click.echo('Usuário demo criado.')
        
        # Criar posts de exemplo
        sample_posts = [
            {
                'title': 'Bem-vindo ao Flask Monolith Template',
                'content': '''# Bem-vindo ao Flask Monolith Template

Este é um template completo para aplicações Flask monolíticas. Ele inclui:

## Funcionalidades

- **Autenticação completa**: Login, registro, perfil de usuário
- **Sistema de posts**: Criação, edição e visualização de artigos
- **Painel administrativo**: Gerenciamento de usuários e conteúdo
- **API REST**: Endpoints JSON para integração
- **Interface responsiva**: Design moderno com Bootstrap 5

## Tecnologias Utilizadas

- Flask 3.0
- SQLAlchemy (SQLite)
- Flask-Login para autenticação
- Bootstrap 5 para UI
- Font Awesome para ícones

## Como usar

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure as variáveis de ambiente
4. Execute: `python app.py`

Este template é perfeito para blogs, sistemas de conteúdo, portfólios e aplicações web em geral.''',
                'category': 'Tutorial',
                'tags': 'flask, python, web development, template',
                'is_published': True,
                'is_featured': True,
                'published_at': datetime.utcnow()
            },
            {
                'title': 'Configurando o Ambiente de Desenvolvimento',
                'content': '''# Configurando o Ambiente de Desenvolvimento

Para começar a trabalhar com este template, você precisa configurar seu ambiente de desenvolvimento.

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

## Instalação

### 1. Clone o repositório

```bash
git clone <repository-url>
cd flask-monolith-template
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e configure as variáveis:

```bash
cp .env.example .env
```

### 5. Inicialize o banco de dados

```bash
flask init-db
flask create-admin
```

### 6. Execute a aplicação

```bash
python app.py
```

Agora você pode acessar a aplicação em `http://localhost:5000`.''',
                'category': 'Tutorial',
                'tags': 'setup, installation, development',
                'is_published': True,
                'published_at': datetime.utcnow()
            },
            {
                'title': 'Arquitetura do Sistema',
                'content': '''# Arquitetura do Sistema

Este template segue uma arquitetura modular e escalável.

## Estrutura de Pastas

```
app/
├── models/          # Modelos de dados
├── routes/          # Blueprints e rotas
├── templates/       # Templates HTML
├── static/          # Arquivos estáticos
└── __init__.py      # Factory da aplicação
```

## Padrões Utilizados

### Factory Pattern
A aplicação utiliza o padrão Factory para criar instâncias configuráveis.

### Blueprint Pattern
As rotas são organizadas em blueprints para melhor modularização:

- `main`: Rotas principais
- `auth`: Autenticação
- `api`: API REST
- `admin`: Administração

### Repository Pattern
Os modelos incluem métodos estáticos para operações comuns.

## Banco de Dados

Utiliza SQLAlchemy com SQLite por padrão, mas pode ser facilmente alterado para PostgreSQL, MySQL, etc.

### Modelos

- **User**: Usuários do sistema
- **Post**: Artigos/posts

## Segurança

- Senhas hasheadas com bcrypt
- CSRF protection
- JWT para API
- Validação de entrada

## Performance

- Paginação automática
- Lazy loading de relacionamentos
- Otimização de queries''',
                'category': 'Arquitetura',
                'tags': 'architecture, patterns, design',
                'is_published': True,
                'published_at': datetime.utcnow()
            }
        ]
        
        for post_data in sample_posts:
            # Verificar se post já existe
            existing_post = Post.query.filter_by(title=post_data['title']).first()
            if not existing_post:
                post = Post(
                    title=post_data['title'],
                    content=post_data['content'],
                    user_id=demo_user.id,
                    category=post_data['category'],
                    tags=post_data['tags'],
                    is_published=post_data['is_published'],
                    is_featured=post_data.get('is_featured', False),
                    published_at=post_data.get('published_at')
                )
                db.session.add(post)
        
        db.session.commit()
        click.echo('Dados de exemplo inseridos com sucesso!')
        
    except Exception as e:
        click.echo(f'Erro ao inserir dados: {str(e)}')
        db.session.rollback()

@click.command()
@with_appcontext
def list_users():
    """Listar todos os usuários"""
    users = User.query.all()
    
    if not users:
        click.echo('Nenhum usuário encontrado.')
        return
    
    click.echo('\nUsuários cadastrados:')
    click.echo('-' * 80)
    click.echo(f'{'ID':<5} {'Username':<15} {'Email':<25} {'Nome':<20} {'Admin':<8} {'Ativo':<8}')
    click.echo('-' * 80)
    
    for user in users:
        admin_status = 'Sim' if user.is_admin else 'Não'
        active_status = 'Sim' if user.is_active else 'Não'
        
        click.echo(f'{user.id:<5} {user.username:<15} {user.email:<25} {user.get_full_name():<20} {admin_status:<8} {active_status:<8}')
    
    click.echo('-' * 80)
    click.echo(f'Total: {len(users)} usuários')

@click.command()
@with_appcontext
def list_posts():
    """Listar todos os posts"""
    posts = Post.query.all()
    
    if not posts:
        click.echo('Nenhum post encontrado.')
        return
    
    click.echo('\nPosts cadastrados:')
    click.echo('-' * 100)
    click.echo(f'{'ID':<5} {'Título':<30} {'Autor':<15} {'Categoria':<15} {'Status':<10} {'Criado':<12}')
    click.echo('-' * 100)
    
    for post in posts:
        status = 'Publicado' if post.is_published else 'Rascunho'
        created = post.created_at.strftime('%d/%m/%Y')
        title = post.title[:27] + '...' if len(post.title) > 30 else post.title
        
        click.echo(f'{post.id:<5} {title:<30} {post.author.username:<15} {post.category or "N/A":<15} {status:<10} {created:<12}')
    
    click.echo('-' * 100)
    click.echo(f'Total: {len(posts)} posts')

@click.command()
@click.argument('username')
@with_appcontext
def make_admin(username):
    """Tornar usuário administrador"""
    user = User.find_by_username(username)
    
    if not user:
        click.echo(f'Usuário "{username}" não encontrado.')
        return
    
    if user.is_admin:
        click.echo(f'Usuário "{username}" já é administrador.')
        return
    
    try:
        user.is_admin = True
        db.session.commit()
        click.echo(f'Usuário "{username}" agora é administrador.')
        
    except Exception as e:
        click.echo(f'Erro ao tornar usuário administrador: {str(e)}')
        db.session.rollback()

@click.command()
@click.argument('username')
@with_appcontext
def remove_admin(username):
    """Remover privilégios de administrador"""
    user = User.find_by_username(username)
    
    if not user:
        click.echo(f'Usuário "{username}" não encontrado.')
        return
    
    if not user.is_admin:
        click.echo(f'Usuário "{username}" não é administrador.')
        return
    
    try:
        user.is_admin = False
        db.session.commit()
        click.echo(f'Privilégios de administrador removidos de "{username}".')
        
    except Exception as e:
        click.echo(f'Erro ao remover privilégios: {str(e)}')
        db.session.rollback()

@click.command()
@with_appcontext
def stats():
    """Mostrar estatísticas da aplicação"""
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    admin_users = User.query.filter_by(is_admin=True).count()
    
    total_posts = Post.query.count()
    published_posts = Post.query.filter_by(is_published=True).count()
    draft_posts = Post.query.filter_by(is_published=False).count()
    
    total_views = sum(post.views_count for post in Post.query.all())
    total_likes = sum(post.likes_count for post in Post.query.all())
    
    click.echo('\n📊 Estatísticas da Aplicação')
    click.echo('=' * 40)
    
    click.echo('\n👥 Usuários:')
    click.echo(f'  Total: {total_users}')
    click.echo(f'  Ativos: {active_users}')
    click.echo(f'  Administradores: {admin_users}')
    
    click.echo('\n📝 Posts:')
    click.echo(f'  Total: {total_posts}')
    click.echo(f'  Publicados: {published_posts}')
    click.echo(f'  Rascunhos: {draft_posts}')
    
    click.echo('\n📈 Engajamento:')
    click.echo(f'  Total de visualizações: {total_views}')
    click.echo(f'  Total de curtidas: {total_likes}')
    
    if published_posts > 0:
        avg_views = total_views / published_posts
        avg_likes = total_likes / published_posts
        click.echo(f'  Média de visualizações por post: {avg_views:.1f}')
        click.echo(f'  Média de curtidas por post: {avg_likes:.1f}')
    
    click.echo('\n')

# Registrar comandos
def register_commands(app):
    """Registrar comandos CLI na aplicação"""
    app.cli.add_command(init_db)
    app.cli.add_command(reset_db)
    app.cli.add_command(create_admin)
    app.cli.add_command(seed_data)
    app.cli.add_command(list_users)
    app.cli.add_command(list_posts)
    app.cli.add_command(make_admin)
    app.cli.add_command(remove_admin)
    app.cli.add_command(stats)