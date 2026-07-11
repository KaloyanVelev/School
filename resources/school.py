from flask_restful import Resource
from managers.School import SchoolManager
from unittest import result
from flask import request, jsonify
from exceptions import AuthError
from managers.auth import auth
from schemas.request.auth import ScoolAddSchema, AddDirectorsSchema
from utils.decorator import validate_schema,permission_required


class SchoolsResource(Resource):
    @auth.login_required
    @permission_required("admin")
    def get(self):
        try:
            result = {}
            result = SchoolManager.schools_list()
            return result, 200

        except AuthError as error:
            response = jsonify({'error': error.message})
            response.status_code = error.status_code
            return response
        except ValueError as error:
            response = jsonify({'error': str(error)})
            response.status_code=400
            return response

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
        except ValueError as error:
            response = jsonify({'error': str(error)})
            response.status_code=400
            return response


class DirectorsResource(Resource):

    @auth.login_required
    @permission_required("admin")
    @validate_schema(AddDirectorsSchema)
    def post(self):
        try:
            provided_data = request.get_json()
            result = SchoolManager.add_school_director(provided_data)

            return result, 200

        except AuthError as error:
            response = jsonify({'error': error.message})
            response.status_code = error.status_code
            return response
        except ValueError as error:
            response = jsonify({'error': str(error)})
            response.status_code=400
            return response
    @auth.login_required
    @permission_required("admin")
    def get(self):
        try:
            result =  {}
            result = SchoolManager.list_school_directors()
            return result, 200

        except AuthError as error:
            response = jsonify({'error': error.message})
            response.status_code = error.status_code
            return response
        except ValueError as error:
            response = jsonify({'error': str(error)})
            response.status_code=400
            return response
