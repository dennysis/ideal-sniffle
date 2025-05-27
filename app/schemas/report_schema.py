from marshmallow import Schema, fields

class ReportSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    date = fields.Date(required=True)
    donor_name = fields.Str(required=True, data_key="donorName")
    amount = fields.Float(required=True)
    usage = fields.Str(required=True)
    usage_date = fields.Date(required=True, data_key="usageDate")
    created_at = fields.DateTime(dump_only=True)
