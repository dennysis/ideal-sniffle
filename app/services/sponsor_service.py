# app/services/sponsor_service.py
from app import db
from app.models.sponsored_child import SponsoredChild

def create_sponsored_child(data):
    """Create a new sponsored child record"""
    try:
        # Validate required fields
        if not data.get('name'):
            raise ValueError('Child name is required')
        
        # Create new sponsored child instance
        child = SponsoredChild(
            name=data.get('name'),
            image_url=data.get('imageUrl'),
            goal_amount=float(data.get('goalAmount', 0)),
            short_description=data.get('shortDescription'),
            full_content=data.get('fullContent')
        )
        
        # Add to database session
        db.session.add(child)
        db.session.commit()
        
        return child
        
    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        raise e

def get_all_sponsored_children():
    """Get all sponsored children"""
    try:
        return SponsoredChild.query.all()
    except Exception as e:
        raise e

def get_sponsored_child_by_id(child_id):
    """Get a specific sponsored child by ID"""
    try:
        return SponsoredChild.query.get(child_id)
    except Exception as e:
        raise e

def update_sponsored_child(child_id, data):
    """Update a sponsored child record"""
    try:
        child = SponsoredChild.query.get(child_id)
        if not child:
            raise ValueError('Child not found')
        
        # Update fields if provided
        if 'name' in data:
            child.name = data['name']
        if 'imageUrl' in data:
            child.image_url = data['imageUrl']
        if 'goalAmount' in data:
            child.goal_amount = float(data['goalAmount'])
        if 'shortDescription' in data:
            child.short_description = data['shortDescription']
        if 'fullContent' in data:
            child.full_content = data['fullContent']
        
        db.session.commit()
        return child
        
    except Exception as e:
        db.session.rollback()
        raise e

def delete_sponsored_child(child_id):
    """Delete a sponsored child record"""
    try:
        child = SponsoredChild.query.get(child_id)
        if not child:
            raise ValueError('Child not found')
        
        db.session.delete(child)
        db.session.commit()
        return True
        
    except Exception as e:
        db.session.rollback()
        raise e