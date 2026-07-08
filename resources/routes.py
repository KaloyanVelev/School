from resources.user import UserRegisterResource, UserLogInResource, TestResource
routes = [
    (UserRegisterResource, '/register'),
    (UserLogInResource, '/login'),
    (TestResource, '/test')
]