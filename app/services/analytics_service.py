from datetime import datetime, timedelta
from sqlalchemy import func, extract
from app import db
from app.models.donation import Donation
from app.models.orphanage import Orphanage
from app.models.user import User

class AnalyticsService:
    @staticmethod
    def get_orphanage_analytics(orphanage_id, period_months=12):
        """Get analytics for a specific orphanage"""
        try:
            # Calculate date range
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=period_months * 30)
            
            # Get donations for this orphanage in the period
            donations = Donation.query.filter(
                Donation.orphanage_id == orphanage_id,
                Donation.status == 'completed',
                Donation.created_at >= start_date
            ).all()
            
            # Calculate basic metrics
            total_donations = sum(d.amount for d in donations)
            donation_count = len(donations)
            average_donation = total_donations / donation_count if donation_count > 0 else 0
            
            # Monthly breakdown
            monthly_data = db.session.query(
                func.date_trunc('month', Donation.created_at).label('month'),
                func.sum(Donation.amount).label('total'),
                func.count(Donation.id).label('count')
            ).filter(
                Donation.orphanage_id == orphanage_id,
                Donation.status == 'completed',
                Donation.created_at >= start_date
            ).group_by(
                func.date_trunc('month', Donation.created_at)
            ).order_by('month').all()
            
            monthly_breakdown = [
                {
                    'month': month.isoformat(),
                    'total': float(total),
                    'count': count
                }
                for month, total, count in monthly_data
            ]
            
            # Top donors (non-anonymous)
            top_donors_data = db.session.query(
                User.name,
                func.sum(Donation.amount).label('total_donated')
            ).join(
                Donation, User.id == Donation.donor_id
            ).filter(
                Donation.orphanage_id == orphanage_id,
                Donation.status == 'completed',
                Donation.is_anonymous == False,
                Donation.created_at >= start_date
            ).group_by(
                User.id, User.name
            ).order_by(
                func.sum(Donation.amount).desc()
            ).limit(5).all()
            
            top_donors = [
                {
                    'name': name,
                    'total_donated': float(total)
                }
                for name, total in top_donors_data
            ]
            
            return {
                'success': True,
                'analytics': {
                    'period_months': period_months,
                    'total_donations': total_donations,
                    'donation_count': donation_count,
                    'average_donation': average_donation,
                    'monthly_breakdown': monthly_breakdown,
                    'top_donors': top_donors
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_platform_analytics():
        """Get platform-wide analytics"""
        try:
            # Basic counts
            total_orphanages = Orphanage.query.filter_by(is_active=True).count()
            total_donors = User.query.filter_by(role='donor', is_active=True).count()
            
            # All completed donations
            completed_donations = Donation.query.filter_by(status='completed').all()
            total_donations = sum(d.amount for d in completed_donations)
            total_donation_count = len(completed_donations)
            average_donation = total_donations / total_donation_count if total_donation_count > 0 else 0
            
            # Recent 30 days
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_donations = Donation.query.filter(
                Donation.status == 'completed',
                Donation.created_at >= thirty_days_ago
            ).all()
            
            recent_total = sum(d.amount for d in recent_donations)
            recent_count = len(recent_donations)
            
            return {
                'success': True,
                'analytics': {
                    'total_orphanages': total_orphanages,
                    'total_donors': total_donors,
                    'total_donations': total_donations,
                    'total_donation_count': total_donation_count,
                    'average_donation': average_donation,
                    'recent_30_days': {
                        'donations': recent_total,
                        'count': recent_count
                    }
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def generate_donation_report(orphanage_id, report_type='monthly'):
        """Generate donation report for an orphanage"""
        try:
            # Calculate date range based on report type
            end_date = datetime.utcnow()
            
            if report_type == 'monthly':
                start_date = end_date - timedelta(days=30)
                period_name = "Monthly"
            elif report_type == 'quarterly':
                start_date = end_date - timedelta(days=90)
                period_name = "Quarterly"
            elif report_type == 'yearly':
                start_date = end_date - timedelta(days=365)
                period_name = "Yearly"
            else:
                return {'success': False, 'error': 'Invalid report type'}
            
            # Get orphanage info
            orphanage = Orphanage.query.get(orphanage_id)
            if not orphanage:
                return {'success': False, 'error': 'Orphanage not found'}
            
            # Get donations for the period
            donations = Donation.query.filter(
                Donation.orphanage_id == orphanage_id,
                Donation.status == 'completed',
                Donation.created_at >= start_date
            ).order_by(Donation.created_at.desc()).all()
            
            # Calculate metrics
            total_amount = sum(d.amount for d in donations)
            donation_count = len(donations)
            average_donation = total_amount / donation_count if donation_count > 0 else 0
            
            # Donation details
            donation_details = [
                {
                    'id': d.id,
                    'amount': d.amount,
                    'currency': d.currency,
                    'donor_name': d.donor.name if d.donor and not d.is_anonymous else 'Anonymous',
                    'message': d.message,
                    'date': d.created_at.isoformat(),
                    'payment_method': d.payment_method
                }
                for d in donations
            ]
            
            report = {
                'report_id': f"RPT_{orphanage_id}_{report_type}_{end_date.strftime('%Y%m%d')}",
                'orphanage': {
                    'id': orphanage.id,
                    'name': orphanage.name,
                    'location': orphanage.location
                },
                'period': {
                    'type': report_type,
                    'name': period_name,
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                },
                'summary': {
                    'total_amount': total_amount,
                    'donation_count': donation_count,
                    'average_donation': average_donation
                },
                'donations': donation_details,
                'generated_at': datetime.utcnow().isoformat()
            }
            
            return {'success': True, 'report': report}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
