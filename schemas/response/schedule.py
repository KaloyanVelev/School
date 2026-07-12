from marshmallow import Schema, fields

class ScheduleResponseSchema(Schema):
    id = fields.String(dump_only=True)
    day_of_week = fields.String(dump_only=True)
    start_time = fields.Time(dump_only=True, format="%H:%M")
    end_time = fields.Time(dump_only=True, format="%H:%M")
    class_number = fields.Integer(dump_only=True)
    room_number = fields.Integer(dump_only=True)
    class_id = fields.String(dump_only=True)
    subject_id = fields.String(dump_only=True)
    teacher_id = fields.String(dump_only=True)
