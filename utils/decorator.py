from marshmallow import Schema, fields
from flask import request
from flask_restful import abort
from marshmallow import ValidationError
from managers.auth import auth
from functools import wraps


def permission_required(required_permission):
    def decorator(function):
        @wraps(function)
        def decorator_function(*args, **kwargs):
            current_user = auth.current_user()
            if current_user.permission.value == "admin":
                return function(*args, **kwargs)

            if current_user.permission.value != required_permission:
                abort(403)
            return function(*args, **kwargs)
        return decorator_function
    return decorator



def validate_schema(schema):
    def decorator(function):
        @wraps(function)
        def decorator_function(*args, **kwargs):
            schema_obj = schema()
            data = request.get_json()
            errors = schema_obj.validate(data)
            if errors:
                raise ValidationError(errors)
            return function(*args, **kwargs)
        return decorator_function
    return decorator