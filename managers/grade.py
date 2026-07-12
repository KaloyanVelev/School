from database import db
from models.grade import GradeModel
from models.student import StudentModel
from models.user import UserModel
from models.school_subject import SchoolSubjectModel
from models.enums import UserRole

class GradeManager:
    @staticmethod
    def add_grade(data):
        student_user_id = data.get('student_id')
        subject_id = data.get('subject_id')
        teacher_user_id = data.get('teacher_id')
        grade_value = data.get('grade')
        comment = data.get('comment')

        student_entry = StudentModel.query.filter_by(student_id=student_user_id).first()
        if not student_entry:
            raise ValueError(f"Student with user ID {student_user_id} not found in student entries.")

        teacher = db.session.get(UserModel, teacher_user_id)
        if not teacher or teacher.permission != UserRole.TEACHER:
            raise ValueError(f"Teacher with user ID {teacher_user_id} not found or is not a teacher.")

        subject = db.session.get(SchoolSubjectModel, subject_id)
        if not subject:
            raise ValueError(f"Subject with ID {subject_id} not found.")

        grade = GradeModel(
            value=grade_value,
            comment=comment,
            student_id=student_entry.id,
            subject_id=subject_id,
            teacher_id=teacher_user_id
        )
        db.session.add(grade)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise ValueError("Failed to add grade.")
        
        return grade

    @staticmethod
    def get_student_grades(student_user_id):

        student_entry = StudentModel.query.filter_by(student_id=student_user_id).first()
        if not student_entry:
            raise ValueError(f"Student with user ID {student_user_id} not found in student entries.")
        
        grades = GradeModel.query.filter_by(student_id=student_entry.id).all()
        return grades

    @staticmethod
    def edit_grade(grade_id, data):
        grade_entry = db.session.get(GradeModel, grade_id)
        if not grade_entry:
            raise ValueError(f"Grade with ID {grade_id} not found.")

        if 'grade' in data:
            grade_entry.value = data['grade']
        if 'comment' in data:
            grade_entry.comment = data['comment']
        
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise ValueError("Failed to edit grade.")
        
        return {
            "message": f"Grade {grade_id} updated successfully.",
            "grade_id": grade_entry.id
        }

    @staticmethod
    def delete_grade(grade_id):
        grade_entry = db.session.get(GradeModel, grade_id)
        if not grade_entry:
            raise ValueError(f"Grade with ID {grade_id} not found.")
        
        db.session.delete(grade_entry)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise ValueError("Failed to delete grade.")
        
        return {"message": f"Grade {grade_id} deleted successfully."}
