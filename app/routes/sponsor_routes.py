# app/routes/sponsor_routes.py
from flask import Blueprint, request, jsonify, current_app
from app.services.sponsor_service import create_sponsored_child, get_all_sponsored_children
from app.models.sponsored_child import SponsoredChild

sponsor_bp = Blueprint('sponsor', __name__)

@sponsor_bp.route('/sponsor-child', methods=['GET'])
def get_sponsored_children_route():
    """Get all sponsored children"""
    try:
        # Use the service function instead of direct query
        children = get_all_sponsored_children()
        
        # Convert to list of dictionaries
        children_data = []
        for child in children:
            child_dict = {
                'id': child.id,
                'name': child.name,
                'imageUrl': child.image_url,
                'goalAmount': child.goal_amount,
                'shortDescription': child.short_description,
                'fullContent': child.full_content
            }
            # Only add timestamps if they exist in the model
            if hasattr(child, 'created_at') and child.created_at:
                child_dict['created_at'] = child.created_at.isoformat()
            if hasattr(child, 'updated_at') and child.updated_at:
                child_dict['updated_at'] = child.updated_at.isoformat()
            
            children_data.append(child_dict)
        
        return jsonify(children_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching sponsored children: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch sponsored children',
            'message': str(e)
        }), 500

@sponsor_bp.route('/sponsor-child', methods=['POST'])
def create_new_sponsored_child():
    """Create a new sponsored child"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Create the sponsored child using the service
        child = create_sponsored_child(data)
        
        # Return the created child data
        child_data = {
            'id': child.id,
            'name': child.name,
            'imageUrl': child.image_url,
            'goalAmount': child.goal_amount,
            'shortDescription': child.short_description,
            'fullContent': child.full_content
        }
        
        return jsonify({
            'message': 'Sponsored child created successfully',
            'child': child_data
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to create sponsored child',
            'message': str(e)
        }), 500

@sponsor_bp.route('/sponsor-child/<int:child_id>', methods=['GET'])
def get_sponsored_child_route(child_id):
    """Get a specific sponsored child by ID"""
    try:
        from app.services.sponsor_service import get_sponsored_child_by_id
        child = get_sponsored_child_by_id(child_id)
        
        if not child:
            return jsonify({'error': 'Child not found'}), 404
        
        child_data = {
            'id': child.id,
            'name': child.name,
            'imageUrl': child.image_url,
            'goalAmount': child.goal_amount,
            'shortDescription': child.short_description,
            'fullContent': child.full_content
        }
        
        # Only add timestamps if they exist
        if hasattr(child, 'created_at') and child.created_at:
            child_data['created_at'] = child.created_at.isoformat()
        if hasattr(child, 'updated_at') and child.updated_at:
            child_data['updated_at'] = child.updated_at.isoformat()
        
        return jsonify(child_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching sponsored child {child_id}: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch sponsored child',
            'message': str(e)
        }), 500