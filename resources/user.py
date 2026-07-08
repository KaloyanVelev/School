from flask import request, jsonify
from flask_restful import Resource

from managers.School import SchoolManager
from managers.auth import auth
from managers.user import UserManager
from schemas.request.auth import UserLogInSchema, UserCreationSchema
from utils.decorator import validate_schema,permission_required
from unittest import result
from flask import Blueprint, request, jsonify
from flask import Blueprint, request, jsonify
from exceptions import AuthError
from managers.auth import auth
from managers.user import UserManager
from schemas.request.auth import UserLogInSchema, UserCreationSchema
from utils.decorator import validate_schema,permission_required


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

class SchoolResource(Resource):
    @auth.login_required
    @permission_required("ADMIN")
    def get(self):
        try:
            result = {}
            result['schools'] = SchoolManager.schools_list()
            return result, 200

        except Exception as e:
            return jsonify({'error': 'something unexpected went wrong'})

    @auth.login_required
    @permission_required("ADMIN")
    def post(self):
        provided_data = request.get_json()

        return

class TestResource(Resource):
    def get(self):
        return jsonify({'message': 'App is working'})