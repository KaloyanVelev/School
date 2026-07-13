from database import db
import uuid


class SchoolModel(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), unique=False, nullable=False)
    institution_address = db.Column(db.String(255), unique=False, nullable=False)