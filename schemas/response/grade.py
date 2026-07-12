from marshmallow import Schema, fields

class GradeResponseSchema(Schema):
    id = fields.String(dump_only=True)
    value = fields.Integer(dump_only=True)
    comment = fields.String(dump_only=True)
    created_on = fields.DateTime(dump_only=True)
    student_id = fields.String(dump_only=True)
    subject_id = fields.String(dump_only=True)
    teacher_id = fields.String(dump_only=True)
