#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para configurar o banco de dados"""

from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    print('Banco de dados criado com sucesso!')