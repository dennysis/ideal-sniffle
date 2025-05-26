from datetime import datetime, timedelta
from app import db
from app.models.donation import Donation
from app.models.orphanage import Orphanage
from app.utils.helpers import generate_transaction_id

class DonationService:
    @staticmethod
    def create_donation(donor_id, donation_data):
        """Create a new donation"""
        try:
            # Verify orphanage exists
            orphanage = Orphanage.query.get(donation_data['orphanage_id'])
            if not orphanage or not orphanage.is_active:
                return {'success': False, 'error': 'Orphanage not found or inactive'}
            
            # Create donation
            donation = Donation(
                donor_id=donor_id,
                orphanage_id=donation_data['orphanage_id'],
                amount=donation_data['amount'],
                currency=donation_data.get('currency', 'USD'),
                payment_method=donation_data['payment_method'],
                message=donation_data.get('message', ''),
                is_anonymous=donation_data.get('is_anonymous', False),
                transaction_id=generate_transaction_id(),
                status='pending'
            )
            
            db.session.add(donation)
            db.session.commit()
            
            return {'success': True, 'donation': donation.to_dict()}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_donation_summary(orphanage_id, period_days=30):
        """Get donation summary for an orphanage"""
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=period_days)
            
            donations = Donation.query.filter(
                Donation.orphanage_id == orphanage_id,
                Donation.status == 'completed',
                Donation.created_at >= start_date
            ).all()
            
            total_amount = sum(d.amount for d in donations)
            donation_count = len(donations)
            average_donation = total_amount / donation_count if donation_count > 0 else 0
            
            summary = {
                'period_days': period_days,
                'total_amount': total_amount,
                'donation_count': donation_count,
                'average_donation': average_donation,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            }
            
            return {'success': True, 'summary': summary}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
