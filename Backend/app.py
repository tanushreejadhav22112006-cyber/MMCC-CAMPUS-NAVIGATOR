from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db, bcrypt
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    CORS(app, 
         origins=['http://localhost:8000', 'http://127.0.0.1:5500', 'http://localhost:5500', 'http://localhost:3000', '*'],
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         supports_credentials=True)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)

    # JWT Configuration - Disable CSRF for API usage
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    app.config['JWT_COOKIE_CSRF_PROTECTION'] = False
    app.config['JWT_ERROR_MESSAGE_KEY'] = 'error'
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.users import users_bp
    from routes.locations import locations_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(locations_bp)
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Campus Navigator API',
            'version': '1.0.0',
            'endpoints': {
                'auth': {
                    'register': 'POST /api/auth/register',
                    'login': 'POST /api/auth/login',
                    'forgot_password': 'POST /api/auth/forgot-password',
                    'reset_password': 'POST /api/auth/reset-password',
                    'verify_token': 'GET /api/auth/verify-token'
                },
                'users': {
                    'profile': 'GET/PUT /api/users/profile',
                    'change_password': 'POST /api/users/change-password'
                },
                'locations': {
                    'all': 'GET /api/locations',
                    'single': 'GET /api/locations/<id>',
                    'search': 'GET /api/locations/search?q=query',
                    'nearby': 'GET /api/locations/nearby?lat=x&lng=y',
                    'types': 'GET /api/locations/types',
                    'save': 'POST /api/locations/<id>/save',
                    'saved': 'GET /api/locations/saved',
                    'unsave': 'DELETE /api/locations/saved/<id>'
                }
            }
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(422)
    def jwt_error(error):
        return jsonify({'error': 'Invalid JWT token'}), 422

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
