import uuid
from database import db

class SchoolSubjectModel(db.Model):
    __tablename__ = 'school_subjects'

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), unique=False, nullable=False)

    school_id = db.Column(db.String(40), db.ForeignKey('schools.id'), nullable=False)