from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.utils.decorators import login_required
from app.schemas.user_schema import UserUpdateSchema
from app.models.user import User
from app import db

user_bp = Blueprint('users', __name__)

@user_bp.route('/<int:user_id>', methods=['GET'])
@login_required
def get_user(current_user, user_id):
    """Get user details"""
    try:
        # Users can only view their own profile or admins can view any
        if current_user.id != user_id and current_user.role != 'admin':
            return jsonify({'error': 'Access denied'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['PUT'])
@login_required
def update_user(current_user, user_id):
    """Update user profile"""
    try:
        # Users can only update their own profile
        if current_user.id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        schema = UserUpdateSchema()
        update_data = schema.load(request.json)
        
        # Update user fields
        if 'name' in update_data:
            user.name = update_data['name']
        if 'phone' in update_data:
            user.phone = update_data['phone']
        
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(current_user, user_id):
    """Delete user account (soft delete)"""
    try:
        # Users can only delete their own account
        if current_user.id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Soft delete - just mark as inactive
        user.is_active = False
        db.session.commit()
        
        return jsonify({
            'message': 'User account deactivated successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500