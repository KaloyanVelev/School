from Scripts.bottle import response
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
from schemas.request.auth import UserLogInSchema, UserCreationSchema,ScoolAddSchema
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
    @permission_required("admin")
    def get(self):
        try:
            result = {}
            result = SchoolManager.schools_list()
            return result, 200

        except AuthError as error:
            return {'error': error.message}, error.status_code

    @auth.login_required
    @permission_required("admin")
    @validate_schema(ScoolAddSchema)
    def post(self):
        try:
            provided_data = request.get_json()
            result = SchoolManager.school_add(provided_data)

            return result, 200
        except AuthError as error:
            response = jsonify({'error': error.message})
            response.status_code = error.status_code
            return  response

class TestResource(Resource):
    def get(self):
        return jsonify({'message': 'App is working'})