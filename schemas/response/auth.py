from marshmallow import fields, validate,Schema
from schemas.bases import BaseUserSchema

class UserResponseSchema(BaseUserSchema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

class SchoolListSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(dump_only=True,validate=validate.Length(min=1, max=150))
    institution_address = fields.String(dump_only=True,validate=validate.Length(min=5, max=500))


class DirectorSchoolListSchema(Schema):
    director_id = fields.String()
    school_id = fields.String()
    school_name = fields.String()

    first_name = fields.String()
    last_name = fields.String()
    affiliated_school_id = fields.String()
    institution_address = fields.String()

class SchoolClassListSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(dump_only=True)
    grade = fields.Integer(dump_only=True)
    letter = fields.String(dump_only=True)

class SchoolSubjectListSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(dump_only=True)

class TeacherListSchema(Schema):
    id = fields.String(dump_only=True)
    first_name = fields.String(dump_only=True)
    last_name = fields.String(dump_only=True)
    email = fields.Email(dump_only=True)

class StudentListSchema(Schema):
    id = fields.String(dump_only=True)
    first_name = fields.String(dump_only=True)
    last_name = fields.String(dump_only=True)
    email = fields.Email(dump_only=True)

class ParentListSchema(Schema):
    id = fields.String(dump_only=True)
    first_name = fields.String(dump_only=True)
    last_name = fields.String(dump_only=True)
    email = fields.Email(dump_only=True)
