from marshmallow import Schema, fields
from schemas.response.schedule import SubjectNestedSchema


class GradeResponseSchema(Schema):
    id = fields.String(dump_only=True)
    value = fields.Integer(dump_only=True)
    comment = fields.String(dump_only=True)
    created_on = fields.DateTime(dump_only=True)
    student_id = fields.String(dump_only=True)
    subject = fields.Nested(SubjectNestedSchema, dump_only=True)
    teacher_id = fields.String(dump_only=True)