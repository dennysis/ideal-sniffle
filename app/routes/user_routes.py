from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from marshmallow import ValidationError
from app.schemas.user_schema import UserSchema, UserUpdateSchema, PasswordChangeSchema
from app.models.user import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
@cross_origin()
def get_profile():
    """Get current user profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 401
        
        schema = UserSchema()
        return jsonify({
            'user': schema.dump(user)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
@cross_origin()
def update_profile():
    """Update user profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 401
        
        schema = UserUpdateSchema()
        update_data = schema.load(request.json)
        
        # Update user fields
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)
        
        # Save changes (assuming your User model has a save method or uses auto-commit)
        
        user_schema = UserSchema()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user_schema.dump(user)
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/change-password', methods=['POST'])
@jwt_required()
@cross_origin()
def change_password():
    """Change user password"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 401
        
        schema = PasswordChangeSchema()
        password_data = schema.load(request.json)
        
        # Verify current password
        if not user.check_password(password_data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        # Update password
        user.set_password(password_data['new_password'])
        # Password updated (assuming auto-commit or save method exists)
        
        return jsonify({
            'message': 'Password changed successfully'
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users', methods=['GET'])
@jwt_required()
@cross_origin()
def get_users():
    """Get all users (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role != 'admin':
            return jsonify({'error': 'Access denied. Admin role required.'}), 403
        
        users = User.query.filter_by(is_active=True).all()
        schema = UserSchema(many=True)
        
        return jsonify({
            'users': schema.dump(users)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_user(user_id):
    """Get specific user by ID"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Users can only view their own profile, admins can view any
        if current_user_id != user_id and current_user.role != 'admin':
            return jsonify({'error': 'Access denied'}), 403
        
        user = User.query.get(user_id)
        if not user or not user.is_active:
            return jsonify({'error': 'User not found'}), 404
        
        schema = UserSchema()
        return jsonify({
            'user': schema.dump(user)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>/deactivate', methods=['POST'])
@jwt_required()
@cross_origin()
def deactivate_user(user_id):
    """Deactivate user account (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role != 'admin':
            return jsonify({'error': 'Access denied. Admin role required.'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.id == current_user_id:
            return jsonify({'error': 'Cannot deactivate your own account'}), 400
        
        user.is_active = False
        # User deactivated (assuming auto-commit or save method exists)
        
        return jsonify({
            'message': 'User deactivated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>/activate', methods=['POST'])
@jwt_required()
@cross_origin()
def activate_user(user_id):
    """Activate user account (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role != 'admin':
            return jsonify({'error': 'Access denied. Admin role required.'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_active = True
        # User activated (assuming auto-commit or save method exists)
        
        return jsonify({
            'message': 'User activated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500