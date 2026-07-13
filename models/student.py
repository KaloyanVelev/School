import uuid
from database import db


class StudentModel(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))

    class_id = db.Column(db.String(40), db.ForeignKey('school_classes.id'), nullable=False)
    student_id = db.Column(db.String(40), db.ForeignKey('users.id'), nullable=False)
