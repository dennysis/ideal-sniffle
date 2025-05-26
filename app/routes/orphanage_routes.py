from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.utils.decorators import login_required
from app.schemas.orphanage_schema import OrphanageSchema, OrphanageCreateSchema, OrphanageUpdateSchema
from app.models.orphanage import Orphanage
from app.models.user import User
from app import db

orphanage_bp = Blueprint('orphanages', __name__)

@orphanage_bp.route('/', methods=['GET'])
def get_all_orphanages():
    """Get all active orphanages (public endpoint)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        orphanages = Orphanage.query.filter_by(is_active=True).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'orphanages': [orphanage.to_dict() for orphanage in orphanages.items],
            'total': orphanages.total,
            'pages': orphanages.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orphanage_bp.route('/<int:orphanage_id>', methods=['GET'])
def get_orphanage(orphanage_id):
    """Get specific orphanage details (public endpoint)"""
    try:
        orphanage = Orphanage.query.filter_by(id=orphanage_id, is_active=True).first()
        if not orphanage:
            return jsonify({'error': 'Orphanage not found'}), 404
        
        return jsonify({
            'orphanage': orphanage.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orphanage_bp.route('/', methods=['POST'])
@login_required
def create_orphanage(current_user):
    """Create new orphanage (only for orphanage role users)"""
    try:
        # Only orphanage role users can create orphanages
        if current_user.role != 'orphanage':
            return jsonify({'error': 'Only orphanage users can create orphanage profiles'}), 403
        
        # Check if user already has an orphanage
        existing_orphanage = Orphanage.query.filter_by(user_id=current_user.id).first()
        if existing_orphanage:
            return jsonify({'error': 'User already has an orphanage profile'}), 400
        
        schema = OrphanageCreateSchema()
        orphanage_data = schema.load(request.json)
        
        # Create new orphanage
        orphanage = Orphanage(
            name=orphanage_data['name'],
            location=orphanage_data['location'],
            description=orphanage_data.get('description'),
            user_id=current_user.id,
            contact_email=orphanage_data.get('contact_email'),
            contact_phone=orphanage_data.get('contact_phone'),
            website=orphanage_data.get('website'),
            registration_number=orphanage_data.get('registration_number'),
            capacity=orphanage_data.get('capacity'),
            current_children=orphanage_data.get('current_children', 0)
        )
        
        db.session.add(orphanage)
        db.session.commit()
        
        return jsonify({
            'message': 'Orphanage created successfully',
            'orphanage': orphanage.to_dict()
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orphanage_bp.route('/my-orphanage', methods=['GET'])
@login_required
def get_my_orphanage(current_user):
    """Get current user's orphanage"""
    try:
        if current_user.role != 'orphanage':
            return jsonify({'error': 'Only orphanage users can access this endpoint'}), 403
        
        orphanage = Orphanage.query.filter_by(user_id=current_user.id).first()
        if not orphanage:
            return jsonify({'error': 'No orphanage profile found'}), 404
        
        return jsonify({
            'orphanage': orphanage.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orphanage_bp.route('/<int:orphanage_id>', methods=['PUT'])
@login_required
def update_orphanage(current_user, orphanage_id):
    """Update orphanage details"""
    try:
        orphanage = Orphanage.query.get(orphanage_id)
        if not orphanage:
            return jsonify({'error': 'Orphanage not found'}), 404
        
        # Only the orphanage owner can update
        if orphanage.user_id != current_user.id:
            return jsonify({'error': 'Access denied'}), 403
        
        schema = OrphanageUpdateSchema()
        update_data = schema.load(request.json)
        
        # Update orphanage fields
        for field in ['name', 'location', 'description', 'contact_email', 
                     'contact_phone', 'website', 'capacity', 'current_children']:
            if field in update_data:
                setattr(orphanage, field, update_data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Orphanage updated successfully',
            'orphanage': orphanage.to_dict()
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orphanage_bp.route('/search', methods=['GET'])
def search_orphanages():
    """Search orphanages by name or location"""
    try:
        query = request.args.get('q', '')
        location = request.args.get('location', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        orphanages_query = Orphanage.query.filter_by(is_active=True)
        
        if query:
            orphanages_query = orphanages_query.filter(
                Orphanage.name.ilike(f'%{query}%')
            )
        
        if location:
            orphanages_query = orphanages_query.filter(
                Orphanage.location.ilike(f'%{location}%')
            )
        
        orphanages = orphanages_query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'orphanages': [orphanage.to_dict() for orphanage in orphanages.items],
            'total': orphanages.total,
            'pages': orphanages.pages,
            'current_page': page,
            'search_query': query,
            'location_filter': location
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
