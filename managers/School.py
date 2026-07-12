from database import db
from models.school import SchoolModel
from models.school_class import SchoolClassModel
from models.user import UserModel
from models.student import StudentModel
from models.school_subject import SchoolSubjectModel
from models.enums import UserRole
from schemas.response.auth import SchoolListSchema, DirectorSchoolListSchema, SchoolClassListSchema, SchoolSubjectListSchema, TeacherListSchema, StudentListSchema


class SchoolManager:
    @staticmethod
    def schools_list():
        try:
            schools = SchoolModel.query.all()
            schema = SchoolListSchema(many=True)
            return schema.dump(schools)

        except Exception:
            raise ValueError('Failed to retrieve schools from the database.')



    @staticmethod
    def _commit_changes(error_message="Database commit failed"):
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise ValueError(error_message)

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

        SchoolManager._commit_changes('Failed to create school.')
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
        user.permission = UserRole.DIRECTOR
        user.affiliated_school_id = provided_school_id
        SchoolManager._commit_changes('Failed to assign director role.')
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
            raise ValueError('Failed to retrieve directors from the database.')


    @staticmethod
    def add_teacher(provided_data):
        provided_teacher_id = provided_data.get('teacher_id')
        provided_school_id = provided_data.get('school_id')
        if not provided_teacher_id:
            raise ValueError('teacher id not provided')
        if not provided_school_id:
            raise ValueError('school id not provided')
        user = db.session.get(UserModel, provided_teacher_id)

        if not user:
            raise ValueError('user not found')
        if user.permission == UserRole.TEACHER:
            raise ValueError('user is already a teacher')
        user.permission = UserRole.TEACHER
        user.affiliated_school_id = provided_school_id
        SchoolManager._commit_changes('Failed to assign teacher role.')
        return {
            'message': f'Added: {user.first_name} {user.last_name} to school with an id of: {provided_school_id} as a Teacher!'
        }

    @staticmethod
    def list_teachers(school_id):
        try:
            teachers = UserModel.query.filter_by(affiliated_school_id=school_id, permission=UserRole.TEACHER).all()
            schema = TeacherListSchema(many=True)
            return schema.dump(teachers)
        except Exception:
            raise ValueError('Failed to retrieve teachers from the database.')

    @staticmethod
    def list_students(school_id):
        try:
            student_entries = db.session.query(StudentModel).join(
                SchoolClassModel, StudentModel.class_id == SchoolClassModel.id
            ).filter(SchoolClassModel.school_id == school_id).all()

            student_user_ids = [entry.student_id for entry in student_entries]
            students = UserModel.query.filter(UserModel.id.in_(student_user_ids)).all()
            
            schema = StudentListSchema(many=True)
            return schema.dump(students)
        except Exception:
            raise ValueError('Failed to retrieve students from the database.')

    @staticmethod
    def list_parents(school_id):
        try:
            parents = UserModel.query.filter_by(affiliated_school_id=school_id, permission=UserRole.PARENT).all()
            schema = ParentListSchema(many=True)
            return schema.dump(parents)
        except Exception:
            raise ValueError('Failed to retrieve parents from the database.')

    @staticmethod
    def add_school_class(provided_data):
        grade = provided_data.get('grade')
        letter = provided_data.get('letter')
        school_id = provided_data.get('school_id')

        if not all([grade, letter, school_id]):
            raise ValueError('Grade, letter, and school ID are required.')

        if not isinstance(grade, int):
            raise ValueError('Grade must be an integer.')

        if not isinstance(letter, str) or len(letter) > 1:
            raise ValueError('Letter must be a single character string.')

        school = db.session.get(SchoolModel, school_id)
        if not school:
            raise ValueError(f"School with id {school_id} not found")

        class_exists = SchoolClassModel.query.filter_by(school_id=school_id, grade=grade, letter=letter.upper()).first()
        if class_exists:
            raise ValueError(f"Class {grade}{letter.upper()} already exists for this school.")

        class_name = f"{grade}{letter.upper()}"
        school_class = SchoolClassModel(
            name=class_name,
            grade=grade,
            letter=letter.upper(),
            school_id=school_id
        )
        db.session.add(school_class)
        SchoolManager._commit_changes("Failed to create school class.")

        return {
            "message": f"Class '{class_name}' created for school '{school.name}'."
        }

    @staticmethod
    def list_school_classes(school_id):
        try:
            classes = SchoolClassModel.query.filter_by(school_id=school_id).all()
            schema = SchoolClassListSchema(many=True)
            return schema.dump(classes)
        except Exception:
            raise ValueError('Failed to retrieve classes from the database.')

    @staticmethod
    def add_school_subject(provided_data):
        subject_name = provided_data.get('name')
        school_id = provided_data.get('school_id')

        if not all([subject_name, school_id]):
            raise ValueError('Subject name and school ID are required.')

        school = db.session.get(SchoolModel, school_id)
        if not school:
            raise ValueError(f"School with id {school_id} not found")

        subject_exists = SchoolSubjectModel.query.filter_by(name=subject_name, school_id=school_id).first()
        if subject_exists:
            raise ValueError(f"Subject '{subject_name}' already exists for this school.")

        school_subject = SchoolSubjectModel(name=subject_name, school_id=school_id)
        db.session.add(school_subject)
        SchoolManager._commit_changes("Failed to create subject.")

        return {
            "message": f"Subject '{school_subject.name}' created for school '{school.name}'."
        }

    @staticmethod
    def list_school_subjects(school_id):
        try:
            subjects = SchoolSubjectModel.query.filter_by(school_id=school_id).all()
            schema = SchoolSubjectListSchema(many=True)
            return schema.dump(subjects)
        except Exception:
            raise ValueError('Failed to retrieve subjects from the database.')
