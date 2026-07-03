from marshmallow import fields, validate, Schema
from marshmallow import ValidationError
from schemas.bases import BaseUserSchema, PasswordValidationMixin


class UserCreationSchema(BaseUserSchema, PasswordValidationMixin):
    password_error ='Password must contain upper case and number'

class UserLogInSchema(Schema, PasswordValidationMixin):
    username = fields.String(required=True, validate=validate.Length(min=4, max=40))
