from enum import Enum as PyEnum


class UserRole(PyEnum):
    STUDENT = 'student'
    TEACHER = 'teacher'
    DIRECTOR = 'director'
    ADMIN = 'admin'
