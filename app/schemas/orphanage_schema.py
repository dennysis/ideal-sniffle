from marshmallow import Schema, fields, validate

class OrphanageSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    location = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    user_id = fields.Int(dump_only=True)
    contact_email = fields.Email(dump_only=True)
    contact_phone = fields.Str(dump_only=True)
    website = fields.Str(dump_only=True)
    registration_number = fields.Str(dump_only=True)
    capacity = fields.Int(dump_only=True)
    current_children = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    total_donations = fields.Float(dump_only=True)
    donation_count = fields.Int(dump_only=True)

class OrphanageCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    location = fields.Str(required=True, validate=validate.Length(min=2, max=200))
    description = fields.Str(validate=validate.Length(max=1000))
    contact_email = fields.Email()
    contact_phone = fields.Str(validate=validate.Length(max=20))
    website = fields.Str(validate=validate.Length(max=200))
    registration_number = fields.Str(validate=validate.Length(max=50))
    capacity = fields.Int(validate=validate.Range(min=1))
    current_children = fields.Int(validate=validate.Range(min=0), missing=0)

class OrphanageUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=2, max=100))
    location = fields.Str(validate=validate.Length(min=2, max=200))
    description = fields.Str(validate=validate.Length(max=1000))
    contact_email = fields.Email()
    contact_phone = fields.Str(validate=validate.Length(max=20))
    website = fields.Str(validate=validate.Length(max=200))
    capacity = fields.Int(validate=validate.Range(min=1))
    current_children = fields.Int(validate=validate.Range(min=0))
