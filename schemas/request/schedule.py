from marshmallow import Schema, fields, validate


class ScheduleAddSchema(Schema):
    day_of_week = fields.String(required=True, validate=validate.OneOf([
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]))
    start_time = fields.Time(required=True, format="%H:%M")
    end_time = fields.Time(required=True, format="%H:%M")
    class_number = fields.Integer(required=True, validate=validate.Range(min=1))
    room_number = fields.Integer(required=True, validate=validate.Range(min=1))
    class_id = fields.String(required=True, validate=validate.Length(equal=36))
    subject_id = fields.String(required=True, validate=validate.Length(equal=36))
    teacher_id = fields.String(required=True, validate=validate.Length(equal=36))