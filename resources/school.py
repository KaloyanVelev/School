from flask_restful import Resource
from managers.School import SchoolManager
from flask import request, jsonify
from exceptions import AuthError
from managers.auth import auth
from schemas.request.auth import ScoolAddSchema, AddDirectorsSchema
from schemas.request.school import SchoolClassAddSchema, SchoolSubjectAddSchema
from schemas.response.auth import SchoolClassListSchema, SchoolSubjectListSchema, TeacherListSchema, StudentListSchema, ParentListSchema
from utils.decorator import validate_schema,permission_required


class SchoolResource(Resource):

   class SchoolsList(Resource):
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

   class SchoolAdd(Resource):
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



class DirectorResource(Resource):

    class DirectorAdd(Resource):
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
                response.status_code = 400
                return response


class SchoolClassResource(Resource):

    class SchoolClassAdd(Resource):
        @auth.login_required
        @permission_required("director")
        @validate_schema(SchoolClassAddSchema)
        def post(self):
            try:
                provided_data = request.get_json()
                result = SchoolManager.add_school_class(provided_data)

                return result, 201

            except AuthError as error:
                response = jsonify({'error': error.message})
                response.status_code = error.status_code
                return response
            except ValueError as error:
                response = jsonify({'error': str(error)})
                response.status_code = 400
                return response

    class SchoolClassList(Resource):
        @auth.login_required
        @permission_required("director")
        def get(self, school_id):
            try:
                classes = SchoolManager.list_school_classes(school_id)
                schema = SchoolClassListSchema(many=True)
                return schema.dump(classes), 200
            except AuthError as error:
                response = jsonify({'error': error.message})
                response.status_code = error.status_code
                return response
            except ValueError as error:
                response = jsonify({'error': str(error)})
                response.status_code = 400
                return response


class SchoolSubjectResource(Resource):

    class SchoolSubjectAdd(Resource):
        @auth.login_required
        @permission_required("director")
        @validate_schema(SchoolSubjectAddSchema)
        def post(self):
            try:
                provided_data = request.get_json()
                result = SchoolManager.add_school_subject(provided_data)

                return result, 201

            except AuthError as error:
                response = jsonify({'error': error.message})
                response.status_code = error.status_code
                return response
            except ValueError as error:
                response = jsonify({'error': str(error)})
                response.status_code = 400
                return response

    class SchoolSubjectList(Resource):
        @auth.login_required
        @permission_required("director")
        def get(self, school_id):
            try:
                subjects = SchoolManager.list_school_subjects(school_id)
                schema = SchoolSubjectListSchema(many=True)
                return schema.dump(subjects), 200
            except AuthError as error:
                response = jsonify({'error': error.message})
                response.status_code = error.status_code
                return response
            except ValueError as error:
                response = jsonify({'error': str(error)})
                response.status_code = 400
                return response

    class GetAllDirectors(Resource):
        @auth.login_required
        @permission_required("admin")
        def get(self):
            try:
                result = {}
                result = SchoolManager.list_school_directors()
                return result, 200

            except AuthError as error:
                response = jsonify({'error': error.message})
                response.status_code = error.status_code
                return response
            except ValueError as error:
                response = jsonify({'error': str(error)})
                response.status_code = 400
                return response



class TeacherResource(Resource):

    class TeacherAdd(Resource):
        @auth.login_required
        @permission_required("director")
        def post(self):
            try:
                provided_data = request.get_json()
                result = SchoolManager.add_teacher(provided_data)

                return result, 200

            except AuthError as error:
                response = jsonify({'error': error.message})
                response.status_code = error.status_code
                return response
            except ValueError as error:
                response = jsonify({'error': str(error)})
                response.status_code = 400
                return response

    class TeacherList(Resource):
        @auth.login_required
        @permission_required("director")
        def get(self, school_id):
            try:
                teachers = SchoolManager.list_teachers(school_id)
                schema = TeacherListSchema(many=True)
                return schema.dump(teachers), 200
            except AuthError as error:
                response = jsonify({'error': error.message})
                response.status_code = error.status_code
                return response
            except ValueError as error:
                response = jsonify({'error': str(error)})
                response.status_code = 400
                return response

class StudentListResource(Resource):
    @auth.login_required
    @permission_required("director")
    def get(self, school_id):
        try:
            students = SchoolManager.list_students(school_id)
            schema = StudentListSchema(many=True)
            return schema.dump(students), 200
        except AuthError as error:
            response = jsonify({'error': error.message})
            response.status_code = error.status_code
            return response
        except ValueError as error:
            response = jsonify({'error': str(error)})
            response.status_code = 400
            return response

class ParentListResource(Resource):
    @auth.login_required
    @permission_required("director")
    def get(self, school_id):
        try:
            parents = SchoolManager.list_parents(school_id)
            schema = ParentListSchema(many=True)
            return schema.dump(parents), 200
        except AuthError as error:
            response = jsonify({'error': error.message})
            response.status_code = error.status_code
            return response
        except ValueError as error:
            response = jsonify({'error': str(error)})
            response.status_code = 400
            return response
