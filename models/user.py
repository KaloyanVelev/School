import uuid
from enum import Enum as PyEnum

from database import db
from models.enums import UserRole
from sqlalchemy import func

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    permission = db.Column(db.Enum(UserRole),nullable=False, default=UserRole.STUDENT)
    created_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(db.DateTime, server_default=func.now())
