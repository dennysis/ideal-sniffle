from flask import Blueprint, request, jsonify
from app import db
from app.models.sponsored_child import SponsorIntent, SponsoredChild  # Import SponsoredChild
from sqlalchemy.exc import SQLAlchemyError

sponsorship_bp = Blueprint('sponsorship_bp', __name__)

@sponsorship_bp.route('/sponsorshipsForm', methods=['GET', 'POST', 'OPTIONS'])
def handle_sponsorships():
    if request.method == 'OPTIONS':
        # Respond OK for CORS preflight
        return '', 200

    if request.method == 'POST':
        data = request.get_json()

        required_fields = ['childId', 'sponsorName', 'sponsorEmail', 'sponsorshipAmount', 'reasonForSponsorship']
        missing = [field for field in required_fields if not data.get(field)]

        if missing:
            return jsonify({'message': f'Missing required fields: {", ".join(missing)}'}), 400

        try:
            intent = SponsorIntent(
                child_id=data['childId'],
                sponsor_name=data['sponsorName'],
                sponsor_email=data['sponsorEmail'],
                sponsor_phone=data.get('sponsorPhone'),
                sponsorship_amount=data['sponsorshipAmount'],
                sponsorship_type=data.get('sponsorshipType', 'monthly'),
                reason_for_sponsorship=data['reasonForSponsorship'],
                additional_message=data.get('additionalMessage')
            )

            db.session.add(intent)
            db.session.commit()

            return jsonify({'message': 'Sponsorship intent submitted successfully.'}), 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'message': 'Failed to save sponsorship intent', 'error': str(e)}), 500

    if request.method == 'GET':
        try:
            intents = SponsorIntent.query.all()
            results = []
            for intent in intents:
                child = SponsoredChild.query.get(intent.child_id)
                child_name = child.name if child else "Unknown Child"

                results.append({
                    'childName': child_name,  # <-- send child's name here
                    'sponsorName': intent.sponsor_name,
                    'sponsorEmail': intent.sponsor_email,
                    'sponsorPhone': intent.sponsor_phone,
                    'sponsorshipAmount': intent.sponsorship_amount,
                    'sponsorshipType': intent.sponsorship_type,
                    'reasonForSponsorship': intent.reason_for_sponsorship,
                    'additionalMessage': intent.additional_message
                })

            return jsonify(results), 200
        except SQLAlchemyError as e:
            return jsonify({'message': 'Failed to fetch sponsorship intents', 'error': str(e)}), 500
