from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    role = fields.Str(required=True, validate=validate.OneOf(['donor', 'orphanage']))
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    phone = fields.Str(validate=validate.Length(max=20))
    created_at = fields.DateTime(dump_only=True)
    is_active = fields.Bool(dump_only=True)

class UserRegistrationSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    phone = fields.Str(required=False, validate=validate.Length(max=20))
    role = fields.Str(required=True, validate=validate.OneOf(['donor', 'orphanage']))

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class UserUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=2, max=100))
    phone = fields.Str(validate=validate.Length(max=20))
