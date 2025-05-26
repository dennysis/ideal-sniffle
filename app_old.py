# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from app import create_app

# load_dotenv()

# # Initialize extensions
# db = SQLAlchemy()
# migrate = Migrate()
# jwt = JWTManager()

# def create_app():
#     app = Flask(__name__)
    
#     # Configuration
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#     app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#     app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-here')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
#     # Initialize extensions with app
#     db.init_app(app)
#     migrate.init_app(app, db)
#     jwt.init_app(app)
#     CORS(app)
    
#     # Import models after db initialization
#     from app.models.user import User
    
#     # Register blueprints
#     from app.routes.auth_routes import auth_bp
#     app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
#     @app.route('/')
#     def home():
#         return {'message': 'Aid Platform API', 'status': 'running'}
    
#     @app.route('/api/health')
#     def health():
#         return {'status': 'healthy', 'message': 'API is running'}
    
#     return app



# app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)
