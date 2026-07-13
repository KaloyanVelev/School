import uuid
from database import db


class ScheduleModel(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    day_of_week = db.Column(db.String(15), unique=False, nullable=False)
    start_time = db.Column(db.Time(), nullable=False)
    end_time = db.Column(db.Time(), nullable=False)
    class_number = db.Column(db.Integer(), nullable=False)
    room_number = db.Column(db.Integer(), nullable=False)

    class_id = db.Column(db.String(40), db.ForeignKey('school_classes.id'), nullable=False)
    subject_id = db.Column(db.String(40), db.ForeignKey('school_subjects.id'), nullable=False)
    teacher_id = db.Column(db.String(40), db.ForeignKey('users.id'), nullable=False)

    subject = db.relationship('SchoolSubjectModel', backref='schedules')

    __table_args__ = (
        db.UniqueConstraint('day_of_week', 'start_time', 'teacher_id', name='uq_teacher_schedule'),
        db.UniqueConstraint('day_of_week', 'start_time', 'class_id', name='uq_class_schedule'),
    )