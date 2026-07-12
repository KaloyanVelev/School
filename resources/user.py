from flask_restful import Resource
from flask import request, jsonify
from exceptions import AuthError
from managers.user import UserManager
from schemas.request.auth import UserLogInSchema, UserCreationSchema
from schemas.response.auth import UserResponseSchema
from utils.decorator import validate_schema
from managers.auth import auth


class UserRegisterResource(Resource):
    @validate_schema(UserCreationSchema)
    def post(self):
        try:
            provided_data = request.get_json()
            result = UserManager.register(provided_data)

            return result, 201

        except AuthError as error:
            response = jsonify({'error': error.message})
            response.status_code = error.status_code
            return response

        except ValueError as error:
            response = jsonify({'error': str(error)})
            response.status_code = 400
            return response


class UserLogInResource(Resource):
    @validate_schema(UserLogInSchema)
    def post(self):
        try:
            provided_data = request.get_json()
            result = UserManager.login(provided_data)

            return result, 200

        except AuthError as error:
            response = jsonify({'error': error.message})
            response.status_code = error.status_code
            return response
        except ValueError as error:
            response = jsonify({'error': str(error)})
            response.status_code = 400
            return response

class UserMeResource(Resource):
    @auth.login_required
    def get(self):
        try:
            current_user = auth.current_user()
            schema = UserResponseSchema()
            return schema.dump(current_user), 200
        except AuthError as error:
            response = jsonify({'error': error.message})
            response.status_code = error.status_code
            return response
        except Exception as e:
            response = jsonify({'error': str(e)})
            response.status_code = 500
            return response

class TestResource(Resource):
    def get(self):
        return jsonify({'message': 'App is working'})