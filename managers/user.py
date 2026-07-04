from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from database import db
from models.user import UserModel
from managers.auth import AuthManager
from models.enums import UserRole
from sqlalchemy import func
from sqlalchemy.exc import InternalError, IntegrityError


class UserManager:
    @staticmethod
    def register(provided_data):
        if UserModel.query.filter_by(email=provided_data['email']).first():
            raise ValueError('Email already registered')

        provided_data['password'] = generate_password_hash(provided_data['password'])

        user = UserModel(**provided_data)

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError('Email already registered!')
        return {
            'message': f'Added User named: {user.username}'
        }



    @staticmethod
    def login(provided_data):
        user = UserModel.query.filter_by(username=provided_data['username']).first()
        if not user or not check_password_hash(user.password,provided_data['password']):
            return jsonify({"error": "invalid credentials"}), 400
        token = AuthManager.encode_token(user)
        return {
            "message": "login successful!",
            "token": token,
            "Permission Level": user.permission.name
        }

