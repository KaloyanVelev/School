from flask_restful import Resource
from flask import request, jsonify
from managers.schedule import ScheduleManager
from managers.auth import auth
from schemas.request.schedule import ScheduleAddSchema
from schemas.response.schedule import ScheduleResponseSchema
from utils.decorator import validate_schema, permission_required
from exceptions import AuthError

class ScheduleResource(Resource):
    class AddSchedule(Resource):
        @auth.login_required
        @permission_required("director")
        @validate_schema(ScheduleAddSchema)
        def post(self):
            try:
                provided_data = request.get_json()
                result = ScheduleManager.add_schedule(provided_data)
                return result, 201
            except AuthError as error:
                response = jsonify({'error': error.message})
                response.status_code = error.status_code
                return response
            except ValueError as error:
                response = jsonify({'error': str(error)})
                response.status_code = 400
                return response

    class StudentScheduleList(Resource):
        @auth.login_required
        @permission_required("student")
        def get(self):
            try:
                current_user_id = auth.current_user().id
                schedules = ScheduleManager.get_schedules_for_student_class(current_user_id)
                schema = ScheduleResponseSchema(many=True)
                return schema.dump(schedules), 200
            except AuthError as error:
                response = jsonify({'error': error.message})
                response.status_code = error.status_code
                return response
            except ValueError as error:
                response = jsonify({'error': str(error)})
                response.status_code = 400
                return response
