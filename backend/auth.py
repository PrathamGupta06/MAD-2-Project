from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") == "admin":
            return fn(*args, **kwargs)
        return {"message": "Admin access required"}, 403
    return wrapper

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print('here')
        verify_jwt_in_request()
        print('there')
        claims = get_jwt()
        print(claims)
        if claims.get("role") == "user" or claims.get("role") == "admin":
            return fn(*args, **kwargs)
        return {"message": "User or admin access required"}, 403
    return wrapper
