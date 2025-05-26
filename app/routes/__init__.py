from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.routes.orphanage_routes import orphanage_bp
from app.routes.donation_routes import donation_bp
from app.routes.notification_routes import notification_bp
from app.routes.analytics_routes import analytics_bp

__all__ = ['auth_bp', 'user_bp', 'orphanage_bp', 'donation_bp', 'notification_bp', 'analytics_bp']