# app/routes/auth.py
from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
from app.services.auth_service import AuthService
from app.models.user import User
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
@cross_origin(origins=['http://localhost:3000'], methods=['GET', 'POST', 'OPTIONS'])
def register():
    """Register a new user"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        logger.info(f"Registration attempt for email: {data.get('email', 'unknown')}")
        
        # Validate required fields on the route level as well
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Additional validation
        if len(data['password']) < 8:
            return jsonify({
                'success': False,
                'error': 'Password must be at least 8 characters long'
            }), 400
        
        if not User.validate_email(data['email']):
            return jsonify({
                'success': False,
                'error': 'Invalid email format'
            }), 400
        
        # Validate phone if provided
        if data.get('phone') and not User.validate_phone(data['phone']):
            return jsonify({
                'success': False,
                'error': 'Invalid phone number format'
            }), 400
        
        # Validate role
        valid_roles = ['donor', 'admin']
        role = data.get('role', 'donor')
        if role not in valid_roles:
            return jsonify({
                'success': False,
                'error': f'Invalid role. Must be one of: {", ".join(valid_roles)}'
            }), 400
        
        # Call service to register user
        result = AuthService.register_user(data)
        
        if result['success']:
            logger.info(f"User registered successfully: {data['email']}")
            return jsonify(result), 201
        else:
            logger.warning(f"Registration failed for {data.get('email', 'unknown')}: {result['error']}")
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error. Please try again.'
        }), 500

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin(origins=['http://localhost:3000'], methods=['GET', 'POST', 'OPTIONS'])
def login():
    """Login user"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        logger.info(f"Login attempt for email: {email}")
        
        # Call service to login user
        result = AuthService.login_user(email, password)
        
        if result['success']:
            logger.info(f"User logged in successfully: {email}")
            return jsonify(result), 200
        else:
            logger.warning(f"Login failed for {email}: {result['error']}")
            return jsonify(result), 401
            
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error. Please try again.'
        }), 500

@auth_bp.route('/check-email', methods=['POST', 'OPTIONS'])
@cross_origin(origins=['http://localhost:3000'], methods=['GET', 'POST', 'OPTIONS'])
def check_email():
    """Check if email already exists"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({
                'success': False,
                'error': 'Email is required'
            }), 400
        
        email = data['email'].strip().lower()
        
        if not User.validate_email(email):
            return jsonify({
                'success': False,
                'error': 'Invalid email format'
            }), 400
        
        user = AuthService.get_user_by_email(email)
        
        return jsonify({
            'success': True,
            'exists': user is not None
        }), 200
        
    except Exception as e:
        logger.error(f"Check email error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error. Please try again.'
        }), 500

@auth_bp.route('/user/<int:user_id>', methods=['GET'])
@cross_origin(origins=['http://localhost:3000'])
def get_user(user_id):
    """Get user by ID"""
    try:
        user = AuthService.get_user_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': user.to_dict_safe()  # Use safe version to avoid sensitive data
        }), 200
        
    except Exception as e:
        logger.error(f"Get user error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error. Please try again.'
        }), 500