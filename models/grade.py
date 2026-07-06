import uuid
from sqlalchemy.sql import func
from database import db

class GradeModel(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    value = db.Column(db.Integer(), nullable=False)
    comment = db.Column(db.Text(), nullable=True)
    created_on = db.Column(db.DateTime, server_default=func.now())

    student_id = db.Column(db.String(40), db.ForeignKey('students.id'), nullable=False)
    teacher_id = db.Column(db.String(40), db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.String(40), db.ForeignKey('school_subjects.id'), nullable=False)



    __table_args__ = (
        db.CheckConstraint('value >= 2 AND value <= 6', name='grade_range_check'),
    )