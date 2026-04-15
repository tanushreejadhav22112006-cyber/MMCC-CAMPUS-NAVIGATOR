from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Location, SavedLocation, User
from math import radians, sin, cos, sqrt, atan2

locations_bp = Blueprint('locations', __name__, url_prefix='/api/locations')


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two points on Earth using Haversine formula"""
    R = 6371000  # Earth's radius in meters
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c


@locations_bp.route('', methods=['GET'])
def get_all_locations():
    """Get all locations with optional filtering"""
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    location_type = request.args.get('type', None)
    search = request.args.get('search', None)
    is_active = request.args.get('is_active', 'true').lower() == 'true'
    
    # Build query
    query = Location.query.filter_by(is_active=is_active)
    
    if location_type:
        query = query.filter_by(location_type=location_type)
    
    if search:
        search_filter = f'%{search}%'
        query = query.filter(
            (Location.name.ilike(search_filter)) |
            (Location.description.ilike(search_filter)) |
            (Location.building.ilike(search_filter))
        )
    
    # Paginate
    pagination = query.order_by(Location.name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    locations = [location.to_dict() for location in pagination.items]
    
    return jsonify({
        'locations': locations,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200


@locations_bp.route('/<int:location_id>', methods=['GET'])
def get_location(location_id):
    """Get a specific location by ID"""
    location = Location.query.get(location_id)
    
    if not location:
        return jsonify({'error': 'Location not found'}), 404
    
    return jsonify(location.to_dict()), 200


@locations_bp.route('', methods=['POST'])
@jwt_required()
def create_location():
    """Create a new location (admin only)"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or current_user.user_type != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'location_type']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Validate location_type
    valid_types = ['building', 'lab', 'classroom', 'facility']
    if data['location_type'] not in valid_types:
        return jsonify({'error': 'Invalid location type'}), 400
    
    # Create location
    location = Location(
        name=data['name'].strip(),
        description=data.get('description', ''),
        location_type=data['location_type'],
        floor=data.get('floor'),
        building=data.get('building'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        image_url=data.get('image_url')
    )
    
    try:
        db.session.add(location)
        db.session.commit()
        
        return jsonify({
            'message': 'Location created successfully',
            'location': location.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create location'}), 500


@locations_bp.route('/<int:location_id>', methods=['PUT'])
@jwt_required()
def update_location(location_id):
    """Update a location (admin only)"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or current_user.user_type != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    location = Location.query.get(location_id)
    if not location:
        return jsonify({'error': 'Location not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'name' in data:
        location.name = data['name'].strip()
    
    if 'description' in data:
        location.description = data['description']
    
    if 'location_type' in data:
        valid_types = ['building', 'lab', 'classroom', 'facility']
        if data['location_type'] not in valid_types:
            return jsonify({'error': 'Invalid location type'}), 400
        location.location_type = data['location_type']
    
    if 'floor' in data:
        location.floor = data['floor']
    
    if 'building' in data:
        location.building = data['building']
    
    if 'latitude' in data:
        location.latitude = data['latitude']
    
    if 'longitude' in data:
        location.longitude = data['longitude']
    
    if 'image_url' in data:
        location.image_url = data['image_url']
    
    if 'is_active' in data:
        location.is_active = data['is_active']
    
    try:
        db.session.commit()
        
        return jsonify({
            'message': 'Location updated successfully',
            'location': location.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update location'}), 500


@locations_bp.route('/<int:location_id>', methods=['DELETE'])
@jwt_required()
def delete_location(location_id):
    """Delete a location (admin only)"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or current_user.user_type != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    location = Location.query.get(location_id)
    if not location:
        return jsonify({'error': 'Location not found'}), 404
    
    try:
        db.session.delete(location)
        db.session.commit()
        
        return jsonify({'message': 'Location deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete location'}), 500


@locations_bp.route('/search', methods=['GET'])
def search_locations():
    """Search locations by query"""
    query = request.args.get('q', '')
    location_type = request.args.get('type', None)
    
    if not query or len(query) < 2:
        return jsonify({'error': 'Search query must be at least 2 characters'}), 400
    
    search_filter = f'%{query}%'
    
    # Build query
    db_query = Location.query.filter_by(is_active=True)
    
    if location_type:
        db_query = db_query.filter_by(location_type=location_type)
    
    db_query = db_query.filter(
        (Location.name.ilike(search_filter)) |
        (Location.description.ilike(search_filter)) |
        (Location.building.ilike(search_filter)) |
        (Location.floor.ilike(search_filter))
    )
    
    locations = db_query.limit(20).all()
    
    return jsonify({
        'locations': [location.to_dict() for location in locations],
        'total': len(locations)
    }), 200


@locations_bp.route('/nearby', methods=['GET'])
def get_nearby_locations():
    """Get locations near given coordinates"""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius = request.args.get('radius', 500, type=int)  # Default 500 meters
    
    if lat is None or lng is None:
        return jsonify({'error': 'Latitude and longitude are required'}), 400
    
    # Get all active locations with coordinates
    locations = Location.query.filter(
        Location.is_active == True,
        Location.latitude.isnot(None),
        Location.longitude.isnot(None)
    ).all()
    
    nearby = []
    for location in locations:
        distance = haversine_distance(
            lat, lng, 
            float(location.latitude), 
            float(location.longitude)
        )
        
        if distance <= radius:
            location_data = location.to_dict()
            location_data['distance'] = round(distance, 2)
            nearby.append(location_data)
    
    # Sort by distance
    nearby.sort(key=lambda x: x['distance'])
    
    return jsonify({
        'locations': nearby,
        'total': len(nearby),
        'search_radius': radius
    }), 200


@locations_bp.route('/types', methods=['GET'])
def get_location_types():
    """Get all location types with counts"""
    from sqlalchemy import func
    
    types = db.session.query(
        Location.location_type,
        func.count(Location.id)
    ).filter_by(is_active=True).group_by(Location.location_type).all()
    
    return jsonify({
        'types': [{'type': t[0], 'count': t[1]} for t in types]
    }), 200


@locations_bp.route('/<int:location_id>/save', methods=['POST'])
@jwt_required()
def save_location(location_id):
    """Save a location to user's favorites"""
    current_user_id = get_jwt_identity()
    
    location = Location.query.get(location_id)
    if not location:
        return jsonify({'error': 'Location not found'}), 404
    
    # Check if already saved
    existing = SavedLocation.query.filter_by(
        user_id=current_user_id,
        location_id=location_id
    ).first()
    
    if existing:
        return jsonify({'error': 'Location already saved'}), 409
    
    data = request.get_json() or {}
    
    saved_location = SavedLocation(
        user_id=current_user_id,
        location_id=location_id,
        notes=data.get('notes', '')
    )
    
    try:
        db.session.add(saved_location)
        db.session.commit()
        
        return jsonify({
            'message': 'Location saved successfully',
            'saved_location': saved_location.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to save location'}), 500


@locations_bp.route('/saved', methods=['GET'])
@jwt_required()
def get_saved_locations():
    """Get current user's saved locations"""
    current_user_id = get_jwt_identity()
    
    saved = SavedLocation.query.filter_by(user_id=current_user_id).all()
    
    return jsonify({
        'saved_locations': [s.to_dict() for s in saved]
    }), 200


@locations_bp.route('/saved/<int:saved_id>', methods=['DELETE'])
@jwt_required()
def unsave_location(saved_id):
    """Remove a saved location"""
    current_user_id = get_jwt_identity()
    
    saved_location = SavedLocation.query.filter_by(
        id=saved_id,
        user_id=current_user_id
    ).first()
    
    if not saved_location:
        return jsonify({'error': 'Saved location not found'}), 404
    
    try:
        db.session.delete(saved_location)
        db.session.commit()
        
        return jsonify({'message': 'Location removed from saved'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to remove saved location'}), 500
