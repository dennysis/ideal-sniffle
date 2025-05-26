from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-here')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    from app.routes.user_routes import user_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.orphanage_routes import orphanage_bp
    from app.routes.analytics_routes import analytics_bp
    from app.routes.donation_routes import donation_bp
    from app.routes.notification_routes import notification_bp

    

    app.register_blueprint(orphanage_bp, url_prefix='/api/orphanages')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(donation_bp, url_prefix='/api/donations')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    
    
    @app.route('/')
    def home():
        return {'message': 'Aid Platform API', 'status': 'running'}
    
    @app.route('/api/health')
    def health():
        return {'status': 'healthy', 'message': 'API is running'}
    
    return app