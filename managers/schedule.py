from database import db
from models.schedule import ScheduleModel
from models.school_class import SchoolClassModel
from models.school_subject import SchoolSubjectModel
from models.user import UserModel
from models.student import StudentModel
from models.enums import UserRole
from datetime import time

class ScheduleManager:
    @staticmethod
    def add_schedule(data):
        day_of_week = data.get('day_of_week')
        start_time_str = data.get('start_time')
        end_time_str = data.get('end_time')
        class_number = data.get('class_number')
        room_number = data.get('room_number')
        class_id = data.get('class_id')
        subject_id = data.get('subject_id')
        teacher_id = data.get('teacher_id')

        try:
            start_time = time.fromisoformat(start_time_str)
            end_time = time.fromisoformat(end_time_str)
        except ValueError:
            raise ValueError("Invalid time format. Expected HH:MM.")

        if start_time >= end_time:
            raise ValueError("Start time must be before end time.")


        school_class = db.session.get(SchoolClassModel, class_id)
        if not school_class:
            raise ValueError(f"School class with id {class_id} not found.")


        school_subject = db.session.get(SchoolSubjectModel, subject_id)
        if not school_subject:
            raise ValueError(f"School subject with id {subject_id} not found.")


        teacher = db.session.get(UserModel, teacher_id)
        if not teacher or teacher.permission != UserRole.TEACHER:
            raise ValueError(f"Teacher with id {teacher_id} not found or is not a teacher.")


        teacher_conflict = ScheduleModel.query.filter(
            ScheduleModel.day_of_week == day_of_week,
            ScheduleModel.start_time == start_time,
            ScheduleModel.teacher_id == teacher_id
        ).first()
        if teacher_conflict:
            raise ValueError(f"Teacher {teacher_id} already has a class at {day_of_week} {start_time_str}.")

        class_conflict = ScheduleModel.query.filter(
            ScheduleModel.day_of_week == day_of_week,
            ScheduleModel.start_time == start_time,
            ScheduleModel.class_id == class_id
        ).first()
        if class_conflict:
            raise ValueError(f"Class {class_id} already has a schedule at {day_of_week} {start_time_str}.")

        schedule_entry = ScheduleModel(
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            class_number=class_number,
            room_number=room_number,
            class_id=class_id,
            subject_id=subject_id,
            teacher_id=teacher_id
        )
        db.session.add(schedule_entry)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise ValueError("Failed to add schedule entry.")
        
        return {
            "message": "Schedule entry added successfully.",
            "schedule_id": schedule_entry.id
        }

    @staticmethod
    def get_schedules_for_student_class(user_id):

        student_entry = StudentModel.query.filter_by(student_id=user_id).first()
        if not student_entry:
            raise ValueError(f"Student entry for user {user_id} not found.")
        
        class_id = student_entry.class_id

        schedules = ScheduleModel.query.filter_by(class_id=class_id).all()
        return schedules
