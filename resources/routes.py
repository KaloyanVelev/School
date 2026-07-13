from resources.user import UserRegisterResource, UserLogInResource, TestResource, UserMeResource, UserListResource
from resources.school import (
    SchoolResource, DirectorResource, TeacherResource, SchoolClassResource, SchoolSubjectResource,
    StudentListResource
)
from resources.student import StudentResource
from resources.schedule import ScheduleResource
from resources.grade import GradeResource

routes = [
    (UserRegisterResource, '/register'),
    (UserLogInResource, '/login'),
    (UserMeResource, '/user/me'),
    (UserListResource, '/users/list'), # New route for listing all users
    (SchoolResource.SchoolAdd, '/school/add'),
    (SchoolResource.SchoolsList, '/schools/list'),
    (SchoolSubjectResource.GetAllDirectors, '/principles/list'),
    (DirectorResource.DirectorAdd, '/principle/add'),
    (TeacherResource.TeacherAdd, '/teacher/add'),
    (TeacherResource.TeacherList, '/school/<string:school_id>/teachers'),
    (SchoolClassResource.SchoolClassAdd, '/school/class/add'),
    (SchoolClassResource.SchoolClassList, '/school/<string:school_id>/classes'),
    (SchoolSubjectResource.SchoolSubjectAdd, '/school/subject/add'),
    (SchoolSubjectResource.SchoolSubjectList, '/school/<string:school_id>/subjects'),
    (StudentResource.AddStudentToClass, '/student/add-to-class'),
    (StudentListResource, '/school/<string:school_id>/students'),
    (ScheduleResource.AddSchedule, '/schedule/add'),
    (ScheduleResource.StudentScheduleList, '/schedule/my-class'),
    (GradeResource.AddGrade, '/grade/add'),
    (GradeResource.StudentGrades, '/grade/my-grades'),
    (GradeResource.EditGrade, '/grade/<string:grade_id>/edit'),
    (GradeResource.DeleteGrade, '/grade/<string:grade_id>/delete'),
    (TestResource, '/test')
]