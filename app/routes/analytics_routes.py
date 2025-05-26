from flask import Blueprint, request, jsonify
from app.utils.decorators import login_required, admin_required
from app.services.analytics_service import AnalyticsService
from app.models.orphanage import Orphanage

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/orphanage/<int:orphanage_id>', methods=['GET'])
@login_required
def get_orphanage_analytics(current_user, orphanage_id):
    """Get analytics for an orphanage"""
    try:
        # Check if user has access to this orphanage
        if current_user.role == 'orphanage':
            orphanage = Orphanage.query.filter_by(
                id=orphanage_id,
                user_id=current_user.id
            ).first()
            if not orphanage:
                return jsonify({'error': 'Access denied'}), 403
        elif current_user.role not in ['admin']:
            return jsonify({'error': 'Access denied'}), 403
        
        period_months = request.args.get('period_months', 12, type=int)
        
        result = AnalyticsService.get_orphanage_analytics(orphanage_id, period_months)
        
        if result['success']:
            return jsonify({
                'analytics': result['analytics']
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/orphanage/<int:orphanage_id>/report', methods=['POST'])
@login_required
def generate_report(current_user, orphanage_id):
    """Generate donation report for an orphanage"""
    try:
        # Check if user owns this orphanage
        if current_user.role == 'orphanage':
            orphanage = Orphanage.query.filter_by(
                id=orphanage_id,
                user_id=current_user.id
            ).first()
            if not orphanage:
                return jsonify({'error': 'Access denied'}), 403
        elif current_user.role not in ['admin']:
            return jsonify({'error': 'Access denied'}), 403
        
        report_type = request.json.get('report_type', 'monthly') if request.json else 'monthly'
        
        if report_type not in ['monthly', 'quarterly', 'yearly']:
            return jsonify({'error': 'Invalid report type'}), 400
        
        result = AnalyticsService.generate_donation_report(orphanage_id, report_type)
        
        if result['success']:
            return jsonify({
                'message': 'Report generated successfully',
                'report': result['report']
            }), 201
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/platform', methods=['GET'])
@login_required
def get_platform_analytics(current_user):
    """Get platform-wide analytics (for system overview)"""
    try:
        # This could be available to all users for transparency
        # or restricted to admins only
        
        result = AnalyticsService.get_platform_analytics()
        
        if result['success']:
            return jsonify({
                'analytics': result['analytics']
            }), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
