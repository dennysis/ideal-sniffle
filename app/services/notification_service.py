from datetime import datetime
from app import db
from app.models.notification import Notification

class NotificationService:
    @staticmethod
    def get_user_notifications(user_id, unread_only=False):
        """Get notifications for a user"""
        try:
            query = Notification.query.filter_by(user_id=user_id)
            
            if unread_only:
                query = query.filter_by(is_read=False)
            
            notifications = query.order_by(Notification.created_at.desc()).all()
            
            return {
                'success': True,
                'notifications': [notification.to_dict() for notification in notifications]
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_unread_count(user_id):
        """Get count of unread notifications for a user"""
        try:
            count = Notification.query.filter_by(
                user_id=user_id,
                is_read=False
            ).count()
            
            return {
                'success': True,
                'unread_count': count
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def mark_notification_read(notification_id, user_id):
        """Mark a specific notification as read"""
        try:
            notification = Notification.query.filter_by(
                id=notification_id,
                user_id=user_id
            ).first()
            
            if not notification:
                return {'success': False, 'error': 'Notification not found'}
            
            if notification.is_read:
                return {'success': False, 'error': 'Notification already read'}
            
            notification.mark_as_read()
            db.session.commit()
            
            return {
                'success': True,
                'notification': notification.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def mark_all_read(user_id):
        """Mark all notifications as read for a user"""
        try:
            notifications = Notification.query.filter_by(
                user_id=user_id,
                is_read=False
            ).all()
            
            count = len(notifications)
            
            for notification in notifications:
                notification.mark_as_read()
            
            db.session.commit()
            
            return {
                'success': True,
                'message': f'Marked {count} notifications as read'
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def delete_notification(notification_id, user_id):
        """Delete a notification"""
        try:
            notification = Notification.query.filter_by(
                id=notification_id,
                user_id=user_id
            ).first()
            
            if not notification:
                return {'success': False, 'error': 'Notification not found'}
            
            db.session.delete(notification)
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Notification deleted successfully'
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def create_notification(user_id, title, message, notification_type, related_id=None, related_type=None):
        """Create a new notification"""
        try:
            notification = Notification(
                user_id=user_id,
                title=title,
                message=message,
                type=notification_type,
                related_id=related_id,
                related_type=related_type
            )
            
            db.session.add(notification)
            db.session.commit()
            
            return {
                'success': True,
                'notification': notification.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
