from flask import Blueprint, request, jsonify
from app import db
from app.models.report import Report
from app.schemas.report_schema import ReportSchema

report_bp = Blueprint('report_bp', __name__, url_prefix='/api/reports')
report_schema = ReportSchema()
report_list_schema = ReportSchema(many=True)

@report_bp.route('/', methods=['GET'])
def get_reports():
    reports = Report.query.order_by(Report.created_at.desc()).all()
    return jsonify({"reports": report_list_schema.dump(reports)})


@report_bp.route('/', methods=['POST'])
def create_report():
    data = request.get_json()
    errors = report_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    report = Report(
        name=data['name'],
        date=data['date'],
        donor_name=data['donorName'],
        amount=data['amount'],
        usage=data['usage'],
        usage_date=data['usageDate']
    )
    db.session.add(report)
    db.session.commit()
    return jsonify(report_schema.dump(report)), 201
