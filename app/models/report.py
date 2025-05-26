from datetime import datetime
from app import db

class DonationReport(db.Model):
    __tablename__ = 'donation_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    orphanage_id = db.Column(db.Integer, db.ForeignKey('orphanages.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Report metadata
    report_type = db.Column(db.String(50), default='monthly')  # monthly, quarterly, annual, custom
    period_start = db.Column(db.DateTime)
    period_end = db.Column(db.DateTime)
    
    # Analytics data (JSON format)
    analytics_data = db.Column(db.JSON)
    
    def to_dict(self):
        """Convert report object to dictionary"""
        return {
            'id': self.id,
            'orphanage_id': self.orphanage_id,
            'title': self.title,
            'summary': self.summary,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'report_type': self.report_type,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'analytics_data': self.analytics_data,
            'orphanage_name': self.orphanage.name if self.orphanage else None
        }
    
    def __repr__(self):
        return f'<DonationReport {self.id}: {self.title}>'