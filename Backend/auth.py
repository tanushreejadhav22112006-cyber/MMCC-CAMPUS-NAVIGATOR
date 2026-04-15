from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, LoginHistory, PasswordResetToken
from datetime import datetime, timedelta
import secrets
import validators

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'email', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400
    
    name = data['name'].strip()
    email = data['email'].strip().lower()
    password = data['password']
    user_type = data.get('user_type', 'student').lower()
    
    # Validate name
    if len(name) < 3:
        return jsonify({'error': 'Name must be at least 3 characters'}), 400
    
    # Validate email
    if not validators.email(email):
        return jsonify({'error': 'Please enter a valid email address'}), 400
    
    # Validate password
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Validate user_type
    valid_user_types = ['student', 'faculty', 'visitor', 'admin']
    if user_type not in valid_user_types:
        return jsonify({'error': 'Invalid user type'}), 400
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create new user
    try:
        new_user = User(
            name=name,
            email=email,
            user_type=user_type
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        # Create access token
        access_token = create_access_token(identity=new_user.id)

        return jsonify({
            'message': 'Registration successful',
            'access_token': access_token,
            'user': new_user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed. Please try again.'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login for students, faculty, and visitors"""
    data = request.get_json()

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Find user
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403

    # Prevent admin users from using regular login
    if user.user_type == 'admin':
        return jsonify({'error': 'Admin accounts must use the admin login page'}), 403

    # Create access token
    access_token = create_access_token(identity=user.id)

    # Record login history
    login_history = LoginHistory(
        user_id=user.id,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent', '')
    )
    db.session.add(login_history)
    db.session.commit()

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin login with fixed credentials"""
    data = request.get_json()

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Find user
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid admin credentials'}), 401

    if not user.is_active:
        return jsonify({'error': 'Admin account is deactivated'}), 403

    # Only allow admin users
    if user.user_type != 'admin':
        return jsonify({'error': 'Access denied. Admin privileges required'}), 403

    # Create access token
    access_token = create_access_token(identity=user.id)

    # Record login history
    login_history = LoginHistory(
        user_id=user.id,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent', '')
    )
    db.session.add(login_history)
    db.session.commit()

    return jsonify({
        'message': 'Admin login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Request password reset"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if not email or not validators.email(email):
        return jsonify({'error': 'Please enter a valid email address'}), 400
    
    # Find user
    user = User.query.filter_by(email=email).first()
    
    # Always return success to prevent email enumeration
    if not user:
        return jsonify({'message': 'If the email exists, a reset link has been sent'}), 200
    
    # Generate reset token
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=1)
    
    # Invalidate any existing tokens
    PasswordResetToken.query.filter_by(user_id=user.id, used=False).update({'used': True})
    
    # Create new token
    reset_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=expires_at
    )
    db.session.add(reset_token)
    db.session.commit()
    
    # In production, send email with reset link
    # For now, just return the token (for development)
    reset_link = f"http://localhost:5000/api/auth/reset-password?token={token}"
    
    # TODO: Implement email sending with Flask-Mail
    # send_reset_email(user.email, user.name, reset_link)
    
    return jsonify({
        'message': 'If the email exists, a reset link has been sent',
        'reset_link': reset_link  # Remove in production
    }), 200


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password using token"""
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')
    
    if not token or not new_password:
        return jsonify({'error': 'Token and new password are required'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Find token
    reset_token = PasswordResetToken.query.filter_by(token=token).first()
    
    if not reset_token or not reset_token.is_valid():
        return jsonify({'error': 'Invalid or expired reset token'}), 400
    
    # Update password
    user = reset_token.user
    user.set_password(new_password)
    reset_token.used = True
    
    db.session.commit()
    
    return jsonify({'message': 'Password reset successful'}), 200


@auth_bp.route('/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    """Verify if JWT token is valid"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_active:
        return jsonify({'error': 'User not found or inactive'}), 404
    
    return jsonify({
        'valid': True,
        'user': user.to_dict()
    }), 200
