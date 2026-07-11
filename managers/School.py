from database import db
from models.school import SchoolModel
from models.user import UserModel
from models.enums import UserRole
from schemas.response.auth import SchoolListSchema, DirectorSchoolListSchema


class SchoolManager:
    @staticmethod
    def schools_list():
        try:
            schools = SchoolModel.query.all()
            schema = SchoolListSchema(many=True)
            return schema.dump(schools)

        except Exception:
            raise ValueError('something went wrong')



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
    @staticmethod
    def add_school_director(provided_data):
        provided_director_id = provided_data.get('director_id')
        provided_school_id = provided_data.get('school_id')
        if not provided_director_id:
            raise ValueError('director id not provided')
        if not provided_school_id:
            raise ValueError('school id not provided')
        user = db.session.get(UserModel, provided_director_id)

        if not user:
            raise ValueError('user not found')
        if user.permission == UserRole.DIRECTOR:
            raise ValueError('user already a director')
        try:
            user.permission = UserRole.DIRECTOR
            user.affiliated_school_id = provided_school_id

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError('Something went wrong in saving your changes')
        return {
            'message': f'Added School director: {user.first_name} {user.last_name} to school: {provided_school_id}'
        }

    @staticmethod
    def list_school_directors():
        try:
            results = db.session.query(
                UserModel.id.label('director_id'),
                UserModel.first_name,
                UserModel.last_name,
                UserModel.affiliated_school_id,
                SchoolModel.id.label('school_id'),
                SchoolModel.name.label('school_name'),
                SchoolModel.institution_address

            ).join(
                SchoolModel,
                UserModel.affiliated_school_id == SchoolModel.id
            ).filter(
                UserModel.permission == UserRole.DIRECTOR
            ).all()
            schema = DirectorSchoolListSchema(many=True)

            return schema.dump(results)

        except Exception:
            raise ValueError('Something went wrong in database extraction')
