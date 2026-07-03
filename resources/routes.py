from flask import Blueprint, request
from managers.auth import auth
from managers.user import UserManager
from schemas.request.auth import UserLogInSchema, UserCreationSchema
from utils.decorator import validate_schema,permission_required



app_bp = Blueprint('api', __name__)

@app_bp.route('/login', methods=['POST'])
@validate_schema(UserLogInSchema)
def user_authentication():
    provided_data = request.get_json()
    return UserManager.login(provided_data)

@app_bp.route('/register', methods=['POST'])
@validate_schema(UserCreationSchema)
def user_registration():
    provided_data = request.get_json()
    return UserManager.register(provided_data)

@app_bp.route('/')
def test():
    return '<p>Database connected</p>'