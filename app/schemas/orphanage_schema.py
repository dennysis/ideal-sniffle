from marshmallow import Schema, fields, validate

class OrphanageSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    location = fields.Str(required=True)
    donation_goal = fields.Float(required=True)
    description = fields.Str(required=True)
    image_url = fields.Str()
    contact_info = fields.Str()
    number_of_children = fields.Int()
    established = fields.Str()
    created_at = fields.DateTime(dump_only=True)
