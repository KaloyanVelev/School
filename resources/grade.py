from flask_restful import Resource
from flask import request, jsonify
from managers.grade import GradeManager
from managers.auth import auth
from schemas.request.grade import GradeAddSchema, GradeEditSchema
from schemas.response.grade import GradeResponseSchema
from utils.decorator import validate_schema, permission_required
from exceptions import AuthError

class GradeResource(Resource):
    class AddGrade(Resource):
        @auth.login_required
        @permission_required("teacher")
        @validate_schema(GradeAddSchema)
        def post(self):
            try:
                provided_data = request.get_json()
                result = GradeManager.add_grade(provided_data)
                schema = GradeResponseSchema()
                return schema.dump(result), 201
            except AuthError as error:
                response = jsonify({'error': error.message})
                response.status_code = error.status_code
                return response
            except ValueError as error:
                response = jsonify({'error': str(error)})
                response.status_code = 400
                return response

    class StudentGrades(Resource):
        @auth.login_required
        @permission_required("student")
        def get(self):
            try:
                current_user_id = auth.current_user().id
                grades = GradeManager.get_student_grades(current_user_id)
                schema = GradeResponseSchema(many=True)
                return schema.dump(grades), 200
            except AuthError as error:
                response = jsonify({'error': error.message})
                response.status_code = error.status_code
                return response
            except ValueError as error:
                response = jsonify({'error': str(error)})
                response.status_code = 400
                return response

    class EditGrade(Resource):
        @auth.login_required
        @permission_required("teacher")
        @validate_schema(GradeEditSchema)
        def put(self, grade_id):
            try:
                provided_data = request.get_json()
                result = GradeManager.edit_grade(grade_id, provided_data)
                return result, 200
            except AuthError as error:
                response = jsonify({'error': error.message})
                response.status_code = error.status_code
                return response
            except ValueError as error:
                response = jsonify({'error': str(error)})
                response.status_code = 400
                return response

    class DeleteGrade(Resource):
        @auth.login_required
        @permission_required("teacher")
        def delete(self, grade_id):
            try:
                result = GradeManager.delete_grade(grade_id)
                return result, 200
            except AuthError as error:
                response = jsonify({'error': error.message})
                response.status_code = error.status_code
                return response
            except ValueError as error:
                response = jsonify({'error': str(error)})
                response.status_code = 400
                return response
