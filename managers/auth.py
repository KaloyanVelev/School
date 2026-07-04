import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app
from models.user import UserModel
from flask_httpauth import HTTPTokenAuth


auth = HTTPTokenAuth(scheme='Bearer')



class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(days=7),
            'sub': user.id
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

@auth.verify_token
def verify_token(token):
    user_id = AuthManager.decode_token(token)
    return UserModel.query.filter_by(id=user_id).first() if user_id else None

@auth.error_handler
def authentication_error(status):
    return {'error': 'invalid or expired token!'}, 401