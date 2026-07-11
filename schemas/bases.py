from marshmallow import Schema, fields, validates, ValidationError
from password_strength import PasswordPolicy

policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1,
)


class BaseUserSchema(Schema):
    email = fields.Email(required=True)


class PasswordValidationMixin:
    password = fields.String(required=True, load_only=True)
    password_error = "Invalid password"

    @validates('password')
    def validate_password(self, password, **kwargs):
        errors =policy.test(password)
        if errors:
            raise ValidationError(self.password_error)
