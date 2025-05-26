from marshmallow import Schema, fields, validate

class DonationSchema(Schema):
    id = fields.Int(dump_only=True)
    donor_id = fields.Int(dump_only=True)
    orphanage_id = fields.Int(dump_only=True)
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    currency = fields.Str(dump_only=True)
    payment_method = fields.Str(dump_only=True)
    message = fields.Str(dump_only=True)
    is_anonymous = fields.Bool(dump_only=True)
    transaction_id = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class DonationCreateSchema(Schema):
    orphanage_id = fields.Int(required=True)
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    currency = fields.Str(missing='USD', validate=validate.OneOf(['USD', 'KES', 'EUR']))
    payment_method = fields.Str(required=True, validate=validate.OneOf(['mpesa', 'paypal', 'stripe']))
    message = fields.Str(missing='')
    is_anonymous = fields.Bool(missing=False)
