from marshmallow import Schema, fields

class SponsoredChildSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    image_url = fields.Str(required=True)
    goal_amount = fields.Float(required=True)
    short_description = fields.Str(required=True)
    full_content = fields.Str(required=True)
