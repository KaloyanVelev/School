from flask import jsonify
from sqlalchemy.sql.functions import user
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
from schemas.response.auth import SchoolListSchema


class SchoolManager:
    @staticmethod
    def schools_list():
        try:
            schools = SchoolModel.query.all()

            # pass many=True because 'schools' is a list of objects
            schema = SchoolListSchema(many=True)
            return schema.dump(schools)  # Returns clean lists of dicts with IDs!

        except Exception as e:
            print("❌ DATABASE/SERIALIZATION ERROR:", e)
            return {'error': 'something unexpected went wrong'}



    @staticmethod
    def school_add(provided_data):
        provided_name = provided_data.get('name')
        provided_institution_address = provided_data.get('institution_address')

        if not provided_name:
            raise ValueError('name not provided')

        if not provided_institution_address:
            raise ValueError('institution address not provided')
        school = SchoolModel(
            name=provided_name,
            institution_address=provided_institution_address
        )
        db.session.add(school)

        try:
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise ValueError('Something went wrong in database commiting')
        return {
            'message': f'Added School named: {school.name} on address: {school.institution_address}',
        }