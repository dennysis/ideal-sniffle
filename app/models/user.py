# app/models/user.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), nullable=False, default='donor')  # Changed default to 'donor'
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    donations_made = db.relationship('Donation', foreign_keys='Donation.donor_id', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        if not password:
            raise ValueError("Password cannot be empty")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        if not password or not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def total_donations(self):
        """Calculate total donations made by this user"""
        try:
            if not self.donations_made:
                return 0.0
            return sum(donation.amount for donation in self.donations_made if donation.status == 'completed')
        except Exception:
            return 0.0
    
    def donation_count(self):
        """Count total number of donations made by this user"""
        try:
            if not self.donations_made:
                return 0
            return len([d for d in self.donations_made if d.status == 'completed'])
        except Exception:
            return 0
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'total_donations': self.total_donations(),
            'donation_count': self.donation_count()
        }
    
    def to_dict_safe(self):
        """Convert user object to dictionary without sensitive information"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        if not email or '@' not in email or '.' not in email:
            return False
        return True
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number format"""
        if not phone:
            return True  # Phone is optional
        # Remove spaces and dashes for validation
        clean_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        return clean_phone.isdigit() and len(clean_phone) >= 10
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def __str__(self):
        return f'{self.name} ({self.email})'