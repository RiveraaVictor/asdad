#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to create admin user programmatically"""

from app import create_app, db
from app.models.user import User

def create_admin_user():
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        admin = User.find_by_username('admin')
        if admin:
            print(f'Admin user "admin" already exists')
            return
        
        # Create admin user
        try:
            admin = User.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                is_admin=True,
                is_active=True,
                email_confirmed=True
            )
            print(f'Administrator "admin" created successfully!')
            print(f'Username: admin')
            print(f'Password: admin123')
            print(f'Email: {admin.email}')
        except Exception as e:
            print(f'Error creating admin: {str(e)}')
            db.session.rollback()

if __name__ == '__main__':
    create_admin_user()