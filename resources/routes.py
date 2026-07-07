from unittest import result

from flask import Blueprint, request, jsonify

from exceptions import AuthError
from managers.auth import auth
from managers.user import UserManager
from schemas.request.auth import UserLogInSchema, UserCreationSchema
from utils.decorator import validate_schema,permission_required


app_bp = Blueprint('api', __name__)

@app_bp.errorhandler(AuthError)
def auth_error_handler(error):
    response = jsonify({'error': error.message})
    response.status_code = error.status_code
    return response
@app_bp.route('/register', methods=['POST'])
@validate_schema(UserCreationSchema)
def user_registration():
    provided_data = request.get_json()

    result = UserManager.register(provided_data)

    return jsonify(result), 201

@app_bp.route('/login', methods=['POST'])
@validate_schema(UserLogInSchema)
def user_authentication():
    provided_data = request.get_json()
    result = UserManager.login(provided_data)

    return jsonify(result), 201

@app_bp.route('/')
def test():
    return '<p>Database connected</p>'