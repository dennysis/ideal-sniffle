from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.user import User
from app.utils.helpers import send_email

# Import db from the main app module
from app import db

class AuthService:
    @staticmethod
    def register_user(user_data):
        """Register a new user"""
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user:
                return {'success': False, 'error': 'Email already registered'}
            
            # Create new user
            user = User(
                role=user_data['role'],
                name=user_data['name'],
                email=user_data['email'],
                phone=user_data.get('phone')
            )
            user.set_password(user_data['password'])
            
            db.session.add(user)
            db.session.commit()
            
            # Send welcome email
            AuthService._send_welcome_email(user)
            
            return {'success': True, 'user': user.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def login_user(email, password):
        """Authenticate user and return tokens"""
        try:
            user = User.query.filter_by(email=email, is_active=True).first()
            
            if not user or not user.check_password(password):
                return {'success': False, 'error': 'Invalid credentials'}
            
            # Create tokens
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            
            return {
                'success': True,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user.to_dict()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def _send_welcome_email(user):
        """Send welcome email to new user"""
        subject = "Welcome to Aid Orphanage Donation System"
        template = f"""
        <h2>Welcome {user.name}!</h2>
        <p>Thank you for joining our orphanage donation platform.</p>
        <p>Your account has been successfully created as a <strong>{user.role}</strong>.</p>
        <p>You can now start {'making donations' if user.role == 'donor' else 'managing your orphanage profile'}.</p>
        """
        send_email(user.email, subject, template)
