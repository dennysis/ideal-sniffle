from marshmallow import Schema, fields, validate

class NotificationSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    title = fields.Str(dump_only=True)
    message = fields.Str(dump_only=True)
    type = fields.Str(dump_only=True)
    is_read = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    read_at = fields.DateTime(dump_only=True)
    related_id = fields.Int(dump_only=True)
    related_type = fields.Str(dump_only=True)

class NotificationCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    message = fields.Str(required=True, validate=validate.Length(min=1))
    type = fields.Str(required=True, validate=validate.OneOf(['donation', 'system', 'reminder', 'alert']))
    related_id = fields.Int()
    related_type = fields.Str(validate=validate.OneOf(['donation', 'orphanage', 'user']))
