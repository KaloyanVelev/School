from resources.user import UserRegisterResource, UserLogInResource, TestResource, SchoolResource
routes = [
    (UserRegisterResource, '/register'),
    (UserLogInResource, '/login'),
    (SchoolResource, '/schools'),
    (TestResource, '/test')
]