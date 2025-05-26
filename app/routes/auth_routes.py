from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from marshmallow import ValidationError
from app.services.auth_service import AuthService
from app.schemas.user_schema import UserRegistrationSchema, UserLoginSchema
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        schema = UserRegistrationSchema()
        user_data = schema.load(request.json)
        
        result = AuthService.register_user(user_data)
        
        if result['success']:
            return jsonify({
                'message': 'User registered successfully',
                'user': result['user']
            }), 201
        else:
            return jsonify({'error': result['error']}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        schema = UserLoginSchema()
        login_data = schema.load(request.json)
        
        result = AuthService.login_user(
            login_data['email'],
            login_data['password']
        )
        
        if result['success']:
            return jsonify({
                'message': 'Login successful',
                'access_token': result['access_token'],
                'refresh_token': result['refresh_token'],
                'user': result['user']
            }), 200
        else:
            return jsonify({'error': result['error']}), 401
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 401
        
        new_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'access_token': new_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user details"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 401
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (client-side token invalidation)"""
    try:
        # In a production app, you might want to blacklist the token
        return jsonify({
            'message': 'Logged out successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500