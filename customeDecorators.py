from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from app_init import app, jwt
from models.Employee import AuthenticationModel
from functools import wraps


def Authentication_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'] == 'Admin':
            return fn(*args, **kwargs)
        elif claims['roles'] == 'Hr':
            return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'] != 'Admin':
            return {"msg": 'Admins only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


def Hr_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'] != 'Hr':
            return {"msg": 'Hr only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user_role = AuthenticationModel.find_by_id(identity)
    if user_role:
        if user_role.role == 'Hr':
            return {'roles': 'Hr'}
        elif user_role.role == 'Admin':
            return {'roles': 'Admin'}
        else:
            return {'roles': 'Employee'}
