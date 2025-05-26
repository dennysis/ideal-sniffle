from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.utils.decorators import login_required, donor_required
from app.schemas.donation_schema import DonationSchema, DonationCreateSchema
from app.services.donation_service import DonationService
from app.models.donation import Donation
from app.models.orphanage import Orphanage

donation_bp = Blueprint('donations', __name__)

@donation_bp.route('', methods=['POST'])
@donor_required
def create_donation(current_user):
    """Make a donation"""
    try:
        schema = DonationCreateSchema()
        donation_data = schema.load(request.json)
        
        result = DonationService.create_donation(current_user.id, donation_data)
        
        if result['success']:
            return jsonify({
                'message': 'Donation created successfully',
                'donation': result['donation']
            }), 201
        else:
            return jsonify({'error': result['error']}), 400
            
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@donation_bp.route('', methods=['GET'])
@login_required
def get_donations(current_user):
    """Get all donations (admin only) or user's donations"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', '')
        
        if current_user.role == 'orphanage':
            # Orphanage admin sees donations to their orphanages
            orphanages = Orphanage.query.filter_by(user_id=current_user.id).all()
            orphanage_ids = [o.id for o in orphanages]
            if orphanage_ids:
                query = Donation.query.filter(Donation.orphanage_id.in_(orphanage_ids))
            else:
                query = Donation.query.filter_by(id=0)  # No results if no orphanages
        else:
            # Donors see their own donations
            query = Donation.query.filter_by(donor_id=current_user.id)
        
        if status:
            query = query.filter_by(status=status)
        
        donations = query.order_by(Donation.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        schema = DonationSchema(many=True)
        
        return jsonify({
            'donations': schema.dump(donations.items),
            'pagination': {
                'page': page,
                'pages': donations.pages,
                'per_page': per_page,
                'total': donations.total
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@donation_bp.route('/<int:donation_id>', methods=['GET'])
@login_required
def get_donation(current_user, donation_id):
    """Get donation details"""
    try:
        donation = Donation.query.get(donation_id)
        if not donation:
            return jsonify({'error': 'Donation not found'}), 404
        
        # Check access permissions
        if current_user.role == 'donor' and donation.donor_id != current_user.id:
            return jsonify({'error': 'Access denied'}), 403
        elif current_user.role == 'orphanage':
            orphanage = Orphanage.query.filter_by(
                id=donation.orphanage_id,
                user_id=current_user.id
            ).first()
            if not orphanage:
                return jsonify({'error': 'Access denied'}), 403
        
        schema = DonationSchema()
        
        return jsonify({
            'donation': schema.dump(donation)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@donation_bp.route('/orphanage/<int:orphanage_id>/summary', methods=['GET'])
@login_required
def get_donation_summary(current_user, orphanage_id):
    """Get donation summary for an orphanage"""
    try:
        # Check if user has access to this orphanage
        if current_user.role == 'orphanage':
            orphanage = Orphanage.query.filter_by(
                id=orphanage_id,
                user_id=current_user.id
            ).first()
            if not orphanage:
                return jsonify({'error': 'Access denied'}), 403
        
        period_days = request.args.get('period_days', 30, type=int)
        
        result = DonationService.get_donation_summary(orphanage_id, period_days)
        
        if result['success']:
            return jsonify(result['summary']), 200
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@donation_bp.route('/callback/mpesa', methods=['POST'])
def mpesa_callback():
    """Handle M-Pesa payment callback"""
    try:
        callback_data = request.json
        return jsonify({'message': 'Callback processed'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
