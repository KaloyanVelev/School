from werkzeug.security import check_password_hash, generate_password_hash
from database import db
from models.user import UserModel
from managers.auth import AuthManager
from models.enums import UserRole
from sqlalchemy.exc import IntegrityError
from sqlalchemy import false
from exceptions import AuthError

DUMMY_PASSWORD_HASH = generate_password_hash("dummy_password")

class UserManager:
    @staticmethod
    def register(provided_data):
        provided_first_name = provided_data.get('first_name')
        provided_last_name = provided_data.get('last_name')
        provided_email = provided_data.get('email')
        provided_password = provided_data.get('password')



        if not provided_first_name:
            raise ValueError('First name not provided')
        if not provided_last_name:
            raise ValueError('Last name not provided')
        if not provided_email:
            raise ValueError('Email not provided')
        if not provided_password:
            raise ValueError('Password not provided')

        if UserModel.query.filter_by(email=provided_data['email']).first():
            raise AuthError('Email already registered', status_code=409)

        password = generate_password_hash(provided_password)

        user = UserModel(
            first_name=provided_data['first_name'],
            last_name=provided_data['last_name'],
            email=provided_data['email'],
            password=password,
            permission=UserRole.STUDENT
        )

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError('Email already registered!')
        return {
            'message': f'Added User named: {user.first_name} {user.last_name}',
        }



    @staticmethod
    def login(provided_data):
        provided_email = provided_data.get('email')
        provided_password = provided_data.get('password')

        if not provided_email:
            raise ValueError('Email not provided')
        if not provided_password:
            raise ValueError('Password not provided')

        user = UserModel.query.filter_by(email=provided_email).first()
        if user:
            is_valid_password = check_password_hash(user.password, provided_password)
        else:
            check_password_hash(DUMMY_PASSWORD_HASH, provided_password)
            is_valid_password =false

        if not user or not is_valid_password:
            raise AuthError("invalid credentials",status_code=401)

        token = AuthManager.encode_token(user)
        return {
            "message": "login successful!",
            "token": token,
            "Permission Level": user.permission.name
        }

