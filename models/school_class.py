import uuid
from database import db


class SchoolClassModel(db.Model):
    __tablename__ = 'school_classes'

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    grade = db.Column(db.Integer(), unique=False, nullable=False)
    letter = db.Column(db.String(1), unique=False, nullable=False)
    name = db.Column(db.String(200), unique=False, nullable=False)

    school_id = db.Column(db.String(40), db.ForeignKey('schools.id'), nullable=False)