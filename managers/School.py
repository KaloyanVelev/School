from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from database import db
from models.school import SchoolModel
from models.user import UserModel
from managers.auth import AuthManager
from models.enums import UserRole
from sqlalchemy import func
from sqlalchemy.exc import InternalError, IntegrityError
from sqlalchemy import func, false
from exceptions import AuthError



class SchoolManager:
    @staticmethod
    def schools_list():
        try:
            schools = SchoolModel.query.all()
            return schools.to_json()
        except Exception as e:
            return jsonify({'error': 'something unexpected goned wrong'})

    @staticmethod
    def school_add(provided_data):

        if not provided_data['name'] or not provided_data['institution_address']:
            return jsonify({'error': 'name and institution_address are required!'})
        try:
            name = provided_data['name']
            institution_address = provided_data['institution_address']

            school = SchoolModel(**provided_data)

        except Exception as e:
            raise e