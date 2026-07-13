from marshmallow import fields, validate, Schema
from schemas.bases import BaseUserSchema, PasswordValidationMixin


class UserCreationSchema(BaseUserSchema, PasswordValidationMixin):
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=40))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=40))
    password_error = 'Password must contain upper case and number'


class UserLogInSchema(Schema, PasswordValidationMixin):
    email = fields.Email(required=True)


class ScoolAddSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=150))
    institution_address = fields.String(required=True, validate=validate.Length(min=5, max=500))


class AddDirectorsSchema(Schema):
    director_id = fields.String(required=True, validate=validate.Length(equal=36))
    school_id = fields.String(required=True, validate=validate.Length(equal=36))