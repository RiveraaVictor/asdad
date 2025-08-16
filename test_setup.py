#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste básico para verificar se o setup está funcionando
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Testar se todas as importações funcionam"""
    print("🔍 Testando importações...")
    
    try:
        # Testar importações principais
        import flask
        import flask_sqlalchemy
        import flask_login
        import flask_wtf
        import flask_mail
        import flask_cors
        import flask_jwt_extended
        import flask_bcrypt
        import flask_migrate
        import python_dotenv
        import click
        
        print("✅ Todas as dependências importadas com sucesso")
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False

def test_app_creation():
    """Testar criação da aplicação"""
    print("\n🏗️  Testando criação da aplicação...")
    
    try:
        # Adicionar diretório atual ao path
        sys.path.insert(0, os.getcwd())
        
        from app import create_app
        
        # Criar aplicação de teste
        app = create_app('testing')
        
        with app.app_context():
            print(f"✅ Aplicação criada: {app.name}")
            print(f"✅ Configuração: {app.config['TESTING']}")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar aplicação: {e}")
        return False

def test_database():
    """Testar conexão com banco de dados"""
    print("\n🗄️  Testando banco de dados...")
    
    try:
        from app import create_app, db
        
        app = create_app('testing')
        
        with app.app_context():
            # Criar tabelas
            db.create_all()
            
            # Testar modelos
            from app.models.user import User
            from app.models.post import Post
            
            print("✅ Modelos importados com sucesso")
            print("✅ Banco de dados configurado")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False

def test_routes():
    """Testar se as rotas estão funcionando"""
    print("\n🛣️  Testando rotas...")
    
    try:
        from app import create_app
        
        app = create_app('testing')
        
        with app.test_client() as client:
            # Testar rota principal
            response = client.get('/')
            print(f"✅ Rota principal: {response.status_code}")
            
            # Testar rota de health check
            response = client.get('/health')
            print(f"✅ Health check: {response.status_code}")
            
            # Testar rota de login
            response = client.get('/auth/login')
            print(f"✅ Rota de login: {response.status_code}")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro nas rotas: {e}")
        return False

def test_files_structure():
    """Testar estrutura de arquivos"""
    print("\n📁 Testando estrutura de arquivos...")
    
    required_files = [
        'app.py',
        'config.py',
        'cli.py',
        'requirements.txt',
        '.env.example',
        'README.md',
        'app/__init__.py',
        'app/models/__init__.py',
        'app/models/user.py',
        'app/models/post.py',
        'app/routes/__init__.py',
        'app/routes/main.py',
        'app/routes/auth.py',
        'app/routes/api.py',
        'app/routes/admin.py',
        'app/templates/base.html',
        'app/templates/main/index.html',
        'app/templates/auth/login.html',
        'app/static/css/style.css',
        'app/static/js/main.js'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print("\n❌ Arquivos ausentes:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ Todos os arquivos necessários estão presentes")
    return True

def main():
    """Função principal de teste"""
    print("🧪 Flask Monolith Template - Teste de Configuração")
    print("="*55)
    
    tests = [
        (test_files_structure, "Estrutura de arquivos"),
        (test_imports, "Importações"),
        (test_app_creation, "Criação da aplicação"),
        (test_database, "Banco de dados"),
        (test_routes, "Rotas")
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func, test_name in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"\n❌ Falha no teste: {test_name}")
        except Exception as e:
            print(f"\n❌ Erro no teste {test_name}: {e}")
    
    print("\n" + "="*55)
    print(f"📊 RESULTADO: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! O setup está funcionando.")
        print("\n✨ Você pode executar a aplicação com:")
        print("   python app.py")
        return True
    else:
        print("⚠️  Alguns testes falharam. Verifique a configuração.")
        return False

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)