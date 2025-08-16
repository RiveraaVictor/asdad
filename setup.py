#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de configuração inicial do Flask Monolith Template
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Executar comando e mostrar progresso"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Concluído")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erro: {e.stderr}")
        return False

def check_python_version():
    """Verificar versão do Python"""
    print("🐍 Verificando versão do Python...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou superior é necessário")
        return False
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def create_env_file():
    """Criar arquivo .env se não existir"""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        print("\n📝 Criando arquivo .env...")
        shutil.copy(env_example, env_file)
        print("✅ Arquivo .env criado a partir do .env.example")
        print("⚠️  Lembre-se de configurar as variáveis no arquivo .env")
    elif env_file.exists():
        print("✅ Arquivo .env já existe")
    else:
        print("❌ Arquivo .env.example não encontrado")
        return False
    return True

def create_directories():
    """Criar diretórios necessários"""
    print("\n📁 Criando diretórios necessários...")
    directories = [
        'uploads',
        'logs',
        'instance',
        'app/static/uploads',
        'migrations/versions'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Criar arquivo .gitkeep para manter diretórios vazios no git
        gitkeep = Path(directory) / '.gitkeep'
        if not gitkeep.exists():
            gitkeep.touch()
    
    print("✅ Diretórios criados")
    return True

def install_dependencies():
    """Instalar dependências Python"""
    if not run_command("pip install -r requirements.txt", "Instalando dependências Python"):
        return False
    return True

def initialize_database():
    """Inicializar banco de dados"""
    commands = [
        ("flask init-db", "Inicializando banco de dados"),
        ("flask seed-data", "Inserindo dados de exemplo")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def create_admin_user():
    """Criar usuário administrador"""
    print("\n👤 Criando usuário administrador...")
    print("Digite as informações do administrador:")
    
    try:
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        first_name = input("Nome: ").strip()
        last_name = input("Sobrenome: ").strip()
        
        if not all([username, email, first_name, last_name]):
            print("❌ Todos os campos são obrigatórios")
            return False
        
        # Criar comando para criar admin
        command = f'flask create-admin --username "{username}" --email "{email}" --first-name "{first_name}" --last-name "{last_name}"'
        
        if run_command(command, "Criando usuário administrador"):
            return True
        else:
            print("⚠️  Você pode criar o administrador manualmente depois com: flask create-admin")
            return True
            
    except KeyboardInterrupt:
        print("\n⚠️  Criação de administrador cancelada")
        print("Você pode criar depois com: flask create-admin")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar administrador: {e}")
        return False

def show_completion_message():
    """Mostrar mensagem de conclusão"""
    print("\n" + "="*60)
    print("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    print("\n📋 Próximos passos:")
    print("\n1. Configure as variáveis no arquivo .env")
    print("2. Execute a aplicação:")
    print("   python app.py")
    print("\n3. Acesse no navegador:")
    print("   http://localhost:5000")
    print("\n4. Conta de demonstração:")
    print("   Username: demo")
    print("   Senha: demo123")
    print("\n📚 Comandos úteis:")
    print("   flask --help          # Ver todos os comandos")
    print("   flask stats           # Ver estatísticas")
    print("   flask list-users      # Listar usuários")
    print("   flask create-admin    # Criar administrador")
    print("\n🐳 Docker (opcional):")
    print("   docker-compose up -d  # Executar com Docker")
    print("\n📖 Documentação completa no README.md")
    print("\n" + "="*60)

def main():
    """Função principal"""
    print("🚀 Flask Monolith Template - Configuração Inicial")
    print("="*50)
    
    # Verificações iniciais
    if not check_python_version():
        sys.exit(1)
    
    # Verificar se estamos no diretório correto
    if not Path('app.py').exists():
        print("❌ Execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    # Passos de configuração
    steps = [
        (create_env_file, "Configuração de ambiente"),
        (create_directories, "Criação de diretórios"),
        (install_dependencies, "Instalação de dependências"),
        (initialize_database, "Inicialização do banco de dados")
    ]
    
    for step_func, step_name in steps:
        if not step_func():
            print(f"\n❌ Falha na etapa: {step_name}")
            print("Verifique os erros acima e tente novamente.")
            sys.exit(1)
    
    # Criar administrador (opcional)
    create_admin = input("\n❓ Deseja criar um usuário administrador agora? (s/N): ").lower().strip()
    if create_admin in ['s', 'sim', 'y', 'yes']:
        create_admin_user()
    
    # Mensagem de conclusão
    show_completion_message()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuração interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)