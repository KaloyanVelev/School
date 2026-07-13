import uuid
from sqlalchemy.sql import func
from database import db


class RemarkModel(db.Model):
    __tablename__ = 'remarks'

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.Text(), nullable=False)
    is_positive = db.Column(db.Boolean(), nullable=False, default=False)
    created_on = db.Column(db.DateTime, server_default=func.now())

    student_id = db.Column(db.String(40), db.ForeignKey('students.id'), nullable=False)
    teacher_id = db.Column(db.String(40), db.ForeignKey('users.id'), nullable=False)
