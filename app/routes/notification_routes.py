from flask import Blueprint, request, jsonify
from app.utils.decorators import login_required
from app.services.notification_service import NotificationService

notification_bp = Blueprint('notifications', __name__)

@notification_bp.route('', methods=['GET'])
@login_required
def get_notifications(current_user):
    """Get user notifications"""
    try:
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        
        result = NotificationService.get_user_notifications(
            current_user.id,
            unread_only=unread_only
        )
        
        if result['success']:
            return jsonify({
                'notifications': result['notifications']
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/unread-count', methods=['GET'])
@login_required
def get_unread_count(current_user):
    """Get count of unread notifications"""
    try:
        result = NotificationService.get_unread_count(current_user.id)
        
        if result['success']:
            return jsonify({
                'unread_count': result['unread_count']
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/<int:notification_id>/read', methods=['PUT'])
@login_required
def mark_notification_read(current_user, notification_id):
    """Mark notification as read"""
    try:
        result = NotificationService.mark_notification_read(
            notification_id,
            current_user.id
        )
        
        if result['success']:
            return jsonify({
                'message': 'Notification marked as read',
                'notification': result['notification']
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/mark-all-read', methods=['PUT'])
@login_required
def mark_all_read(current_user):
    """Mark all notifications as read"""
    try:
        result = NotificationService.mark_all_read(current_user.id)
        
        if result['success']:
            return jsonify({
                'message': result['message']
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/<int:notification_id>', methods=['DELETE'])
@login_required
def delete_notification(current_user, notification_id):
    """Delete notification"""
    try:
        result = NotificationService.delete_notification(
            notification_id,
            current_user.id
        )
        
        if result['success']:
            return jsonify({
                'message': result['message']
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500