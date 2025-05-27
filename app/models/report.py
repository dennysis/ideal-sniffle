from app import db
from datetime import datetime

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    donor_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    usage = db.Column(db.Text, nullable=False)
    usage_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
