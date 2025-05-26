from datetime import datetime
from app import db

class Orphanage(db.Model):
    __tablename__ = 'orphanages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Additional fields
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    website = db.Column(db.String(200))
    registration_number = db.Column(db.String(50))
    capacity = db.Column(db.Integer)
    current_children = db.Column(db.Integer, default=0)
    
    # Relationships
    donations = db.relationship('Donation', foreign_keys='Donation.orphanage_id', lazy=True)
    
    def total_donations(self):
        """Calculate total donations received"""
        return sum(donation.amount for donation in self.donations if donation.status == 'completed')
    
    def donation_count(self):
        """Count total number of donations"""
        return len([d for d in self.donations if d.status == 'completed'])
    
    def to_dict(self):
        """Convert orphanage object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'user_id': self.user_id,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'website': self.website,
            'registration_number': self.registration_number,
            'capacity': self.capacity,
            'current_children': self.current_children,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'total_donations': self.total_donations(),
            'donation_count': self.donation_count()
        }
    
    def __repr__(self):
        return f'<Orphanage {self.name}>'
