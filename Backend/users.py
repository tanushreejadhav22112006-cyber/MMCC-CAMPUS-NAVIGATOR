from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, LoginHistory
from sqlalchemy import func

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_active:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user profile"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_active:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update name if provided
    if 'name' in data:
        name = data['name'].strip()
        if len(name) < 3:
            return jsonify({'error': 'Name must be at least 3 characters'}), 400
        user.name = name
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': user.to_dict()
    }), 200


@users_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change current user password"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_active:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        return jsonify({'error': 'Current and new password are required'}), 400
    
    # Verify current password
    if not user.check_password(current_password):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    if len(new_password) < 6:
        return jsonify({'error': 'New password must be at least 6 characters'}), 400
    
    # Update password
    user.set_password(new_password)
    db.session.commit()
    
    return jsonify({'message': 'Password changed successfully'}), 200


@users_bp.route('/admin/stats', methods=['GET'])
@jwt_required()
def get_admin_stats():
    """Get simple admin statistics"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or not current_user.is_active:
        return jsonify({'error': 'User not found'}), 404

    # Get total users
    total_users = User.query.count()

    # Get active users
    active_users = User.query.filter_by(is_active=True).count()
    inactive_users = total_users - active_users

    # Get total logins
    total_logins = LoginHistory.query.count()

    # Get user type breakdown
    student_count = User.query.filter_by(user_type='student').count()
    faculty_count = User.query.filter_by(user_type='faculty').count()
    visitor_count = User.query.filter_by(user_type='visitor').count()
    admin_count = User.query.filter_by(user_type='admin').count()

    # Get total locations
    from models import Location
    total_locations = 20  # Hardcoded value

    # Get location type breakdown
    building_count = Location.query.filter_by(location_type='building').count()
    lab_count = 7  # Hardcoded value
    classroom_count = Location.query.filter_by(location_type='classroom').count()

    # Get recent logins (last 24 hours)
    from datetime import datetime, timedelta
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_logins_24h = LoginHistory.query.filter(LoginHistory.login_at >= yesterday).count()

    # Get newest user
    newest_user = User.query.order_by(User.created_at.desc()).first()
    newest_user_name = newest_user.name if newest_user else 'N/A'
    newest_user_date = newest_user.created_at.strftime('%Y-%m-%d %H:%M') if newest_user else 'N/A'

    # Get most active user (most logins)
    most_active = db.session.query(
        User.id, User.name, func.count(LoginHistory.id).label('login_count')
    ).join(LoginHistory).group_by(User.id, User.name).order_by(
        func.count(LoginHistory.id).desc()
    ).first()
    most_active_name = most_active.name if most_active else 'N/A'
    most_active_logins = most_active.login_count if most_active else 0

    # Get faculty login stats
    faculty_logins_24h = db.session.query(func.count(LoginHistory.id)).join(
        User, User.id == LoginHistory.user_id
    ).filter(
        User.user_type == 'faculty',
        LoginHistory.login_at >= yesterday
    ).scalar()
    
    faculty_total_logins = db.session.query(func.count(LoginHistory.id)).join(
        User, User.id == LoginHistory.user_id
    ).filter(
        User.user_type == 'faculty'
    ).scalar()

    # Get most recent faculty login
    latest_faculty_login = db.session.query(
        User.name, User.email, LoginHistory.login_at
    ).join(
        LoginHistory, User.id == LoginHistory.user_id
    ).filter(
        User.user_type == 'faculty'
    ).order_by(
        LoginHistory.login_at.desc()
    ).first()
    last_faculty_login_name = latest_faculty_login.name if latest_faculty_login else 'N/A'
    last_faculty_login_time = latest_faculty_login.login_at.strftime('%Y-%m-%d %H:%M') if latest_faculty_login and latest_faculty_login.login_at else 'Never'

    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
        'total_logins': total_logins,
        'recent_logins_24h': recent_logins_24h,
        'student_count': student_count,
        'faculty_count': faculty_count,
        'visitor_count': visitor_count,
        'admin_count': admin_count,
        'total_locations': total_locations,
        'building_count': building_count,
        'lab_count': lab_count,
        'classroom_count': classroom_count,
        'newest_user_name': newest_user_name,
        'newest_user_date': newest_user_date,
        'most_active_name': most_active_name,
        'most_active_logins': most_active_logins,
        'faculty_logins_24h': faculty_logins_24h,
        'faculty_total_logins': faculty_total_logins,
        'last_faculty_login_name': last_faculty_login_name,
        'last_faculty_login_time': last_faculty_login_time
    }), 200


@users_bp.route('/admin/overview', methods=['GET'])
@jwt_required()
def admin_overview():
    """Get admin overview statistics (admin only)"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or current_user.user_type != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    # Get total users
    total_users = User.query.count()

    # Get active users
    active_users = User.query.filter_by(is_active=True).count()

    # Get user type breakdown
    user_type_counts = db.session.query(
        User.user_type,
        func.count(User.id)
    ).group_by(User.user_type).all()

    user_type_dict = {ut[0]: ut[1] for ut in user_type_counts}

    # Get total logins
    total_logins = LoginHistory.query.count()

    # Get total locations (will be fetched from locations endpoint)
    from models import Location
    total_locations = Location.query.count()

    # Get recent user login details
    recent_logins = db.session.query(
        User.id,
        User.name,
        User.email,
        User.user_type,
        func.count(LoginHistory.id).label('login_count')
    ).join(
        LoginHistory, User.id == LoginHistory.user_id
    ).group_by(
        User.id, User.name, User.email, User.user_type
    ).order_by(
        func.max(LoginHistory.login_at).desc()
    ).limit(10).all()

    users_list = [{
        'id': login.id,
        'name': login.name,
        'email': login.email,
        'user_type': login.user_type,
        'login_count': login.login_count
    } for login in recent_logins]

    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'total_locations': total_locations,
        'total_logins': total_logins,
        'user_type_counts': user_type_dict,
        'users': users_list
    }), 200


@users_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """Get all users (admin only)"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or current_user.user_type != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    user_type = request.args.get('user_type', None)
    search = request.args.get('search', None)
    
    # Build query
    query = User.query
    
    if user_type:
        query = query.filter_by(user_type=user_type)
    
    if search:
        search_filter = f'%{search}%'
        query = query.filter(
            (User.name.ilike(search_filter)) | 
            (User.email.ilike(search_filter))
        )
    
    # Paginate
    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    users = [user.to_dict() for user in pagination.items]
    
    return jsonify({
        'users': users,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200


@users_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user details (admin only)"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or current_user.user_type != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()

    # Update fields
    if 'name' in data:
        name = data['name'].strip()
        if len(name) < 3:
            return jsonify({'error': 'Name must be at least 3 characters'}), 400
        user.name = name

    if 'user_type' in data:
        valid_types = ['student', 'faculty', 'visitor', 'admin']
        if data['user_type'] not in valid_types:
            return jsonify({'error': 'Invalid user type'}), 400
        user.user_type = data['user_type']

    if 'is_active' in data:
        user.is_active = data['is_active']

    db.session.commit()

    return jsonify({
        'message': 'User updated successfully',
        'user': user.to_dict()
    }), 200


@users_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete a user (admin only)"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or current_user.user_type != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Prevent deleting own account
    if user_id == current_user_id:
        return jsonify({'error': 'Cannot delete your own account'}), 400

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200
