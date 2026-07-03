from database import db
import uuid

class SubjectModel(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), unique=True, nullable=False)

class ScheduleModel(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    day_of_week = db.Column(db.String(20), nullable=False)
    subject_id = db.Column(db.String(40), db.ForeignKey('subjects.id'), nullable=False)
    teacher_id = db.Column(db.String(40), db.ForeignKey('user.id'), nullable=True)
    grade_level = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
