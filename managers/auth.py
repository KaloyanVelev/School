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
            return {'Expired session!'}, 400
        except jwt.InvalidTokenError:
            return {'Invalid token!'}, 400

@auth.verify_token
def verify_token(token):
    user_id = AuthManager.decode_token(token)
    return UserModel.query.filter_by(id=user_id).first() if user_id else None
