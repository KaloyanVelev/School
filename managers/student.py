from database import db
from models.student import StudentModel
from models.school_class import SchoolClassModel
from models.user import UserModel
from models.enums import UserRole

class StudentManager:
    @staticmethod
    def add_student_to_class(data):
        class_id = data.get('class_id')
        user_id = data.get('student_id')

        school_class = db.session.get(SchoolClassModel, class_id)
        if not school_class:
            raise ValueError(f"School class with id {class_id} not found.")

        user = db.session.get(UserModel, user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found.")
        if user.permission != UserRole.STUDENT:
            raise ValueError(f"User {user_id} is not a student.")

        existing_student_entry = StudentModel.query.filter_by(student_id=user_id).first()
        if existing_student_entry:
            raise ValueError(f"Student {user_id} is already assigned to a class.")

        student_entry = StudentModel(
            class_id=class_id,
            student_id=user_id
        )
        db.session.add(student_entry)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise ValueError("Failed to add student to class.")
        
        return {
            "message": f"Student {user.first_name} {user.last_name} added to class {school_class.name}.",
            "student_entry_id": student_entry.id
        }
