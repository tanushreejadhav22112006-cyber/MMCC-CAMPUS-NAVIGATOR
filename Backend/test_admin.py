"""Test script to verify admin user and credentials"""
from app import create_app
from models import User, db

app = create_app()

with app.app_context():
    # Check if admin exists
    admin = User.query.filter_by(user_type='admin').first()
    
    if admin:
        print(f'✓ Admin user exists')
        print(f'  - Name: {admin.name}')
        print(f'  - Email: {admin.email}')
        print(f'  - User Type: {admin.user_type}')
        print(f'  - Is Active: {admin.is_active}')
        
        # Test password verification
        test_password = 'admin123'
        password_correct = admin.check_password(test_password)
        print(f'  - Password "admin123" correct: {password_correct}')
    else:
        print('✗ Admin user does not exist')
    
    # Count all users by type
    print('\nUser counts by type:')
    for user_type in ['student', 'faculty', 'visitor', 'admin']:
        count = User.query.filter_by(user_type=user_type).count()
        print(f'  - {user_type.capitalize()}: {count}')
