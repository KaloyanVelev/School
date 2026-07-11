from resources.user import UserRegisterResource, UserLogInResource, TestResource
from resources.school import SchoolsResource, DirectorsResource
routes = [
    (UserRegisterResource, '/register'),
    (UserLogInResource, '/login'),
    (SchoolsResource, '/schools'),
    (DirectorsResource, '/principles'),
    (TestResource, '/test')
]