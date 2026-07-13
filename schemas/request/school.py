from marshmallow import Schema, fields, validate


class SchoolClassAddSchema(Schema):
    grade = fields.Integer(required=True, validate=validate.Range(min=1, max=12))
    letter = fields.String(required=True, validate=validate.Length(equal=1))
    school_id = fields.String(required=True, validate=validate.Length(equal=36))


class SchoolSubjectAddSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=200))
    school_id = fields.String(required=True, validate=validate.Length(equal=36))