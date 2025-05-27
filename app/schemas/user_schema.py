# app/schemas/user_schema.py
from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class UserSchema(Schema):
    """Schema for user serialization/deserialization"""
    id = fields.Int(dump_only=True)
    role = fields.Str(required=True, validate=validate.OneOf(['donor', 'orphanage', 'admin', 'user']))
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    phone = fields.Str(validate=validate.Length(max=20))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_active = fields.Bool(dump_only=True)

class UserRegistrationSchema(Schema):
    """Schema for user registration validation"""
    name = fields.Str(
        required=True, 
        validate=[
            validate.Length(min=2, max=100, error="Name must be between 2 and 100 characters"),
            validate.Regexp(r'^[a-zA-Z\s]+$', error="Name can only contain letters and spaces")
        ]
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(max=120, error="Email must not exceed 120 characters")
    )
    password = fields.Str(
        required=True,
        validate=[
            validate.Length(min=8, error="Password must be at least 8 characters long"),
            validate.Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)',
                error="Password must contain at least one lowercase letter, one uppercase letter, and one digit"
            )
        ]
    )
    phone = fields.Str(
        missing=None,
        validate=[
            validate.Length(max=20, error="Phone number must not exceed 20 characters"),
            validate.Regexp(r'^\+?[\d\s\-\(\)]+$', error="Invalid phone number format")
        ],
        allow_none=True
    )
    role = fields.Str(
        required=True,
        validate=validate.OneOf(
            ['donor', 'orphanage', 'admin', 'user'], 
            error="Role must be one of: donor, orphanage, admin, user"
        )
    )

class UserLoginSchema(Schema):
    """Schema for user login validation"""
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=1))

class UserUpdateSchema(Schema):
    """Schema for user profile updates"""
    name = fields.Str(
        validate=[
            validate.Length(min=2, max=100, error="Name must be between 2 and 100 characters"),
            validate.Regexp(r'^[a-zA-Z\s]+$', error="Name can only contain letters and spaces")
        ]
    )
    phone = fields.Str(
        validate=[
            validate.Length(max=20, error="Phone number must not exceed 20 characters"),
            validate.Regexp(r'^\+?[\d\s\-\(\)]+$', error="Invalid phone number format")
        ],
        allow_none=True
    )
    # Email and role changes might require additional verification

class PasswordChangeSchema(Schema):
    """Schema for password change validation"""
    current_password = fields.Str(required=True)
    new_password = fields.Str(
        required=True,
        validate=[
            validate.Length(min=8, error="Password must be at least 8 characters long"),
            validate.Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)',
                error="Password must contain at least one lowercase letter, one uppercase letter, and one digit"
            )
        ]
    )
    confirm_password = fields.Str(required=True)

    @validates_schema
    def validate_passwords_match(self, data, **kwargs):
        """Validate that new password and confirmation match"""
        if data.get('new_password') != data.get('confirm_password'):
            raise ValidationError('New password and confirmation do not match')

# Custom validation functions
def validate_unique_email(email):
    """Check if email is already registered"""
    from app.models.user import User
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        raise ValidationError('Email address is already registered')

def validate_strong_password(password):
    """Additional password strength validation"""
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long')
    
    if not any(c.islower() for c in password):
        raise ValidationError('Password must contain at least one lowercase letter')
    
    if not any(c.isupper() for c in password):
        raise ValidationError('Password must contain at least one uppercase letter')
    
    if not any(c.isdigit() for c in password):
        raise ValidationError('Password must contain at least one digit')
    
    # Check for common weak passwords
    weak_passwords = ['password', '12345678', 'qwerty123', 'admin123']
    if password.lower() in weak_passwords:
        raise ValidationError('Password is too common. Please choose a stronger password')

# Role-based validation
class DonorRegistrationSchema(UserRegistrationSchema):
    """Schema specifically for donor registration"""
    role = fields.Str(missing='donor', validate=validate.Equal('donor'))

class OrphanageRegistrationSchema(UserRegistrationSchema):
    """Schema specifically for orphanage registration"""
    role = fields.Str(missing='orphanage', validate=validate.Equal('orphanage'))
    organization_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=200, error="Organization name must be between 2 and 200 characters")
    )
    organization_type = fields.Str(
        validate=validate.OneOf(
            ['orphanage', 'ngo', 'charity', 'government'], 
            error="Invalid organization type"
        )
    )
    registration_number = fields.Str(
        validate=validate.Length(max=50, error="Registration number must not exceed 50 characters")
    )

class AdminRegistrationSchema(UserRegistrationSchema):
    """Schema specifically for admin registration"""
    role = fields.Str(missing='admin', validate=validate.Equal('admin'))
    organization_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=200, error="Organization name must be between 2 and 200 characters")
    )
    organization_type = fields.Str(
        validate=validate.OneOf(
            ['orphanage', 'ngo', 'charity', 'government'], 
            error="Invalid organization type"
        )
    )
    registration_number = fields.Str(
        validate=validate.Length(max=50, error="Registration number must not exceed 50 characters")
    )