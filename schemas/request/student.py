from marshmallow import Schema, fields, validate

class StudentAddSchema(Schema):
    class_id = fields.String(required=True, validate=validate.Length(equal=36))
    student_id = fields.String(required=True, validate=validate.Length(equal=36))
