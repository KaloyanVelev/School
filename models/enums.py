from enum import Enum as PyEnum

class UserRole(PyEnum):
    STUDENT = 'student'
    PARENT = 'parent'
    TEACHER = 'teacher'
    DIRECTOR = 'director'
    ADMIN = 'admin'