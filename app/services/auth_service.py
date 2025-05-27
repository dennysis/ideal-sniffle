# app/services/auth_service.py
from app.models.user import User
from app import db
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """Service class for handling authentication operations"""
    @staticmethod
    def register_user(user_data):
        """Register a new user with improved error handling"""
        try:
            # Validate data first
            if not user_data:
                return {
                    'success': False,
                    'error': 'No user data provided'
                }
            
            # Check required fields
            required_fields = ['name', 'email', 'password']
            for field in required_fields:
                if field not in user_data or not str(user_data[field]).strip():
                    return {
                        'success': False,
                        'error': f'Missing required field: {field}'
                    }
            
            # Clean and validate email
            email = user_data['email'].strip().lower()
            if '@' not in email:
                return {
                    'success': False,
                    'error': 'Invalid email format'
                }
            
            # Validate password length
            if len(user_data['password']) < 8:
                return {
                    'success': False,
                    'error': 'Password must be at least 8 characters long'
                }
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return {
                    'success': False,
                    'error': 'Email address is already registered'
                }
            
            # Create new user with cleaned data
            user = User(
                name=user_data['name'].strip(),
                email=email,
                phone=user_data.get('phone', '').strip() or None,
                role=user_data.get('role', 'donor')  # Changed default from 'user' to 'donor'
            )
            
            # Set password
            user.set_password(user_data['password'])
            
            # Add to database with explicit commit
            db.session.add(user)
            db.session.commit()
            
            logger.info(f"User registered successfully: {user.email} with role: {user.role}")
            
            return {
                'success': True,
                'user': user.to_dict(),
                'message': 'User registered successfully'
            }
            
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Database integrity error during registration: {str(e)}")
            return {
                'success': False,
                'error': 'Email address is already registered'
            }
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error during user registration: {str(e)}")
            return {
                'success': False,
                'error': f'Registration failed: {str(e)}'
            }
    
    @staticmethod
    def login_user(email, password):
        """
        Authenticate user login
        
        Args:
            email (str): User email
            password (str): User password
            
        Returns:
            dict: Result with success status and user data or error message
        """
        try:
            # Clean email input
            email = email.strip().lower()
            
            # Find user by email
            user = User.query.filter_by(email=email).first()
            
            if not user:
                return {
                    'success': False,
                    'error': 'Invalid email or password'
                }
            
            # Check if user account is active
            if not user.is_active:
                return {
                    'success': False,
                    'error': 'Account is deactivated. Please contact support.'
                }
            
            # Verify password
            if not user.check_password(password):
                return {
                    'success': False,
                    'error': 'Invalid email or password'
                }
            
            logger.info(f"User logged in successfully: {user.email} with role: {user.role}")
            
            return {
                'success': True,
                'user': user.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Error during user login: {str(e)}")
            return {
                'success': False,
                'error': 'Login failed. Please try again.'
            }
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        
        Args:
            user_id (int): User ID
            
        Returns:
            User: User object or None
        """
        try:
            return User.query.get(user_id)
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {str(e)}")
            return None
    
    @staticmethod
    def get_user_by_email(email):
        """
        Get user by email
        
        Args:
            email (str): User email
            
        Returns:
            User: User object or None
        """
        try:
            return User.query.filter_by(email=email.strip().lower()).first()
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {str(e)}")
            return None
    
    @staticmethod
    def update_user_profile(user_id, update_data):
        """
        Update user profile
        
        Args:
            user_id (int): User ID
            update_data (dict): Data to update
            
        Returns:
            dict: Result with success status and updated user data or error message
        """
        try:
            user = User.query.get(user_id)
            
            if not user:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            # Update allowed fields
            if 'name' in update_data and update_data['name'].strip():
                user.name = update_data['name'].strip()
            if 'phone' in update_data:
                user.phone = update_data['phone'].strip() or None
            
            db.session.commit()
            
            logger.info(f"User profile updated: {user.email}")
            
            return {
                'success': True,
                'user': user.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating user profile for ID {user_id}: {str(e)}")
            return {
                'success': False,
                'error': 'Profile update failed. Please try again.'
            }
    
    @staticmethod
    def change_password(user_id, current_password, new_password):
        """
        Change user password
        
        Args:
            user_id (int): User ID
            current_password (str): Current password
            new_password (str): New password
            
        Returns:
            dict: Result with success status or error message
        """
        try:
            user = User.query.get(user_id)
            
            if not user:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            # Verify current password
            if not user.check_password(current_password):
                return {
                    'success': False,
                    'error': 'Current password is incorrect'
                }
            
            # Validate new password
            if len(new_password) < 8:
                return {
                    'success': False,
                    'error': 'New password must be at least 8 characters long'
                }
            
            # Set new password
            user.set_password(new_password)
            db.session.commit()
            
            logger.info(f"Password changed for user: {user.email}")
            
            return {
                'success': True,
                'message': 'Password changed successfully'
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error changing password for user ID {user_id}: {str(e)}")
            return {
                'success': False,
                'error': 'Password change failed. Please try again.'
            }
    
    @staticmethod
    def deactivate_user(user_id):
        """
        Deactivate user account
        
        Args:
            user_id (int): User ID
            
        Returns:
            dict: Result with success status or error message
        """
        try:
            user = User.query.get(user_id)
            
            if not user:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            user.is_active = False
            db.session.commit()
            
            logger.info(f"User account deactivated: {user.email}")
            
            return {
                'success': True,
                'message': 'Account deactivated successfully'
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deactivating user ID {user_id}: {str(e)}")
            return {
                'success': False,
                'error': 'Account deactivation failed. Please try again.'
            }
    
    @staticmethod
    def get_users_by_role(role, page=1, per_page=10):
        """
        Get users by role with pagination
        
        Args:
            role (str): User role
            page (int): Page number
            per_page (int): Items per page
            
        Returns:
            dict: Paginated user data
        """
        try:
            users = User.query.filter_by(role=role, is_active=True)\
                        .paginate(page=page, per_page=per_page, error_out=False)
            
            return {
                'success': True,
                'users': [user.to_dict() for user in users.items],
                'total': users.total,
                'pages': users.pages,
                'current_page': page
            }
            
        except Exception as e:
            logger.error(f"Error getting users by role {role}: {str(e)}")
            return {
                'success': False,
                'error': 'Failed to retrieve users'
            }