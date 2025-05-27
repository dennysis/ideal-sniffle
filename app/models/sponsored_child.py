# app/models/sponsored_child.py
from app import db

class SponsoredChild(db.Model):
    __tablename__ = 'sponsored_children'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    goal_amount = db.Column(db.Float, nullable=False, default=0.0)
    short_description = db.Column(db.Text, nullable=True)
    full_content = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<SponsoredChild {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'imageUrl': self.image_url,
            'goalAmount': self.goal_amount,
            'shortDescription': self.short_description,
            'fullContent': self.full_content
        }
    

# app/models/sponsored_child.py
from app import db
from datetime import datetime

class SponsorIntent(db.Model):
    __tablename__ = 'sponsor_intents'

    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, nullable=False)
    sponsor_name = db.Column(db.String(100), nullable=False)
    sponsor_email = db.Column(db.String(120), nullable=False)
    sponsor_phone = db.Column(db.String(20))
    sponsorship_amount = db.Column(db.Float, nullable=False)
    sponsorship_type = db.Column(db.String(50), default='monthly')
    reason_for_sponsorship = db.Column(db.Text, nullable=False)
    additional_message = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
