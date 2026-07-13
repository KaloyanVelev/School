import uuid
from database import db
from models.enums import UserRole
from sqlalchemy import func


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    permission = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    affiliated_school_id = db.Column(db.String(40), db.ForeignKey('schools.id'), nullable=True)
    created_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(db.DateTime, server_default=func.now())
