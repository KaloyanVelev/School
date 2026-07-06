from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from database import db
from models.user import UserModel
from managers.auth import AuthManager
from models.enums import UserRole
from sqlalchemy import func, false
from exceptions import AuthError

DUMMY_PASSWORD_HASH = generate_password_hash("dummy_password")

class UserManager:
    @staticmethod
    def register(provided_data):
        if UserModel.query.filter_by(email=provided_data['email']).first():
            raise AuthError('Email already registered', status_code=409)

        provided_data['password'] = generate_password_hash(provided_data['password'])

        user = UserModel(**provided_data)

        db.session.add(user)
        db.session.commit()
        return {
            'message': f'Added User named: {user.username}'
        }



    @staticmethod
    def login(provided_data):
        user = UserModel.query.filter_by(username=provided_data['username']).first()
        if user:
            is_valid_password = check_password_hash(user.password, provided_data['password'])
        else:
            check_password_hash(DUMMY_PASSWORD_HASH, provided_data['password'])
            is_valid_password =false

        if not user or not is_valid_password:
            raise AuthError("invalid credentials",status_code=401)

        token = AuthManager.encode_token(user)
        return {
            "message": "login successful!",
            "token": token,
            "Permission Level": user.permission.name
        }

