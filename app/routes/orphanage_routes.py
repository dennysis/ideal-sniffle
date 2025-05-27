from flask import Blueprint, request, jsonify
from app import db
from app.models.orphanage import Orphanage
from app.schemas.orphanage_schema import OrphanageSchema

orphanage_bp = Blueprint('orphanage_bp', __name__)
orphanage_schema = OrphanageSchema()

@orphanage_bp.route('', methods=['GET', 'POST'])
@orphanage_bp.route('/', methods=['GET', 'POST'])
def handle_orphanages():
    if request.method == 'GET':
        all_orphanages = Orphanage.query.all()
        result = orphanage_schema.dump(all_orphanages, many=True)
        return jsonify(result), 200

    elif request.method == 'POST':
        data = request.get_json()
        errors = orphanage_schema.validate(data)
        if errors:
            return jsonify(errors), 400

        user_id = None  # no login, so set to None or default

        new_orphanage = Orphanage(
            name=data['name'],
            location=data['location'],
            donation_goal=data['donation_goal'],
            description=data['description'],
            image_url=data.get('image_url'),
            contact_info=data.get('contact_info'),
            number_of_children=data.get('number_of_children'),
            established=data.get('established'),
            user_id=user_id
        )

        db.session.add(new_orphanage)
        db.session.commit()

        return jsonify(orphanage_schema.dump(new_orphanage)), 201
