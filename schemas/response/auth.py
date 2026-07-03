from marshmallow import fields
from schemas.bases import BaseUserSchema

class UserResponseSchema(BaseUserSchema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)