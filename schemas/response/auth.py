from marshmallow import fields, validate,Schema
from schemas.bases import BaseUserSchema

class UserResponseSchema(BaseUserSchema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class SchoolListSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(dump_only=True,validate=validate.Length(min=1, max=150))
    institution_address = fields.String(dump_only=True,validate=validate.Length(min=5, max=500))