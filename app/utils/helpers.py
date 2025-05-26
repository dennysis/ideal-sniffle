import uuid
import secrets
from datetime import datetime

def generate_transaction_id():
    """Generate unique transaction ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_part = secrets.token_hex(4).upper()
    return f"TXN{timestamp}{random_part}"

def send_email(to_email, subject, html_body):
    """Send email using Flask-Mail"""
    try:
        # This is a placeholder - you'll need to configure Flask-Mail
        print(f"Sending email to {to_email}")
        print(f"Subject: {subject}")
        print(f"Body: {html_body}")
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def format_currency(amount, currency='USD'):
    """Format currency amount"""
    return f"{currency} {amount:,.2f}"

def validate_phone_number(phone):
    """Basic phone number validation"""
    import re
    pattern = r'^\+?[\d\s\-\(\)]{10,15}$'
    return bool(re.match(pattern, phone)) if phone else True

def paginate_query(query, page, per_page=20):
    """Paginate SQLAlchemy query"""
    return query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
