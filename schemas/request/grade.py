from marshmallow import Schema, fields, validate

class GradeAddSchema(Schema):
    student_id = fields.String(required=True, validate=validate.Length(equal=36))
    subject_id = fields.String(required=True, validate=validate.Length(equal=36))
    teacher_id = fields.String(required=True, validate=validate.Length(equal=36))
    grade = fields.Integer(required=True, validate=validate.Range(min=2, max=6))
    comment = fields.String(required=False, validate=validate.Length(max=255))

class GradeEditSchema(Schema):
    grade = fields.Integer(required=False, validate=validate.Range(min=2, max=6))
    comment = fields.String(required=False, validate=validate.Length(max=255))

class GradeDeleteSchema(Schema):
    pass
