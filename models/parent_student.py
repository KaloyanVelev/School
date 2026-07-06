import uuid
from database import db

class ParentStudentModel(db.Model):
    __tablename__ = 'parent_students'

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))

    parent_id = db.Column(db.String(40), db.ForeignKey('users.id'), nullable=False)
    student_id = db.Column(db.String(40), db.ForeignKey('users.id'), nullable=False)