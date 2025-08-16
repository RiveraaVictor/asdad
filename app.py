#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Monolith Template - Aplicação Principal

Um template completo para aplicações Flask monolíticas com:
- Autenticação e autorização
- Sistema de posts/blog
- Painel administrativo
- API REST
- Interface moderna
"""

import os
from app import create_app, db

if __name__ == '__main__':
    app = create_app()
    host = os.getenv('APP_HOST', '127.0.0.1')
    port = int(os.getenv('APP_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)