from datetime import datetime
from app import db

class Donation(db.Model):
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    orphanage_id = db.Column(db.Integer, db.ForeignKey('orphanages.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    payment_method = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text)
    is_anonymous = db.Column(db.Boolean, default=False)
    transaction_id = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - Fix the overlapping warnings
    donor = db.relationship('User', foreign_keys=[donor_id], overlaps="donations_made")
    orphanage = db.relationship('Orphanage', foreign_keys=[orphanage_id], overlaps="donations")
    
    def to_dict(self):
        """Convert donation object to dictionary"""
        return {
            'id': self.id,
            'donor_id': self.donor_id,
            'orphanage_id': self.orphanage_id,
            'amount': self.amount,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'message': self.message,
            'is_anonymous': self.is_anonymous,
            'transaction_id': self.transaction_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'donor_name': self.donor.name if self.donor and not self.is_anonymous else 'Anonymous',
            'orphanage_name': self.orphanage.name if self.orphanage else None
        }
    
    def __repr__(self):
        return f'<Donation {self.transaction_id}: {self.amount} {self.currency}>'
