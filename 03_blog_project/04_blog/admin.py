from functools import wraps
from flask import abort
from flask_login import current_user

#Create admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != "admin":
            return abort(403)
        #Otherwise continue with the route function
        return f(*args, **kwargs)        
    return decorated_function