from datetime import datetime
from app import db

class Orphanage(db.Model):
    __tablename__ = 'orphanages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(300), nullable=True)
    donation_goal = db.Column(db.Float, nullable=True)  # changed to Float for precision
    is_active = db.Column(db.Boolean, default=True)
    established = db.Column(db.String(10), nullable=True)  # added to match React form

    # Contact info from React form (combined into one field, but kept full fields too)
    contact_info = db.Column(db.Text)
    contact_email = db.Column(db.String(120), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    
    # Additional details
    website = db.Column(db.String(200), nullable=True)
    registration_number = db.Column(db.String(50), nullable=True)
    capacity = db.Column(db.Integer, nullable=True)
    current_children = db.Column(db.Integer, default=0)
    number_of_children = db.Column(db.Integer, nullable=True)  # from form
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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
            'image_url': self.image_url,
            'donation_goal': self.donation_goal,
            'is_active': self.is_active,
            'established': self.established,
            'contact_info': self.contact_info,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'website': self.website,
            'registration_number': self.registration_number,
            'capacity': self.capacity,
            'current_children': self.current_children,
            'number_of_children': self.number_of_children,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'total_donations': self.total_donations(),
            'donation_count': self.donation_count()
        }
    
    def __repr__(self):
        return f'<Orphanage {self.name}>'
