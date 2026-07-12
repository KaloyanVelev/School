from flask_restful import Resource
from flask import request, jsonify
from managers.student import StudentManager
from managers.auth import auth
from schemas.request.student import StudentAddSchema
from utils.decorator import validate_schema, permission_required
from exceptions import AuthError

class StudentResource(Resource):
    class AddStudentToClass(Resource):
        @auth.login_required
        @permission_required("director")
        @validate_schema(StudentAddSchema)
        def post(self):
            try:
                provided_data = request.get_json()
                result = StudentManager.add_student_to_class(provided_data)
                return result, 201
            except AuthError as error:
                response = jsonify({'error': error.message})
                response.status_code = error.status_code
                return response
            except ValueError as error:
                response = jsonify({'error': str(error)})
                response.status_code = 400
                return response
