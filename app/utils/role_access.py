from functools import wraps
from app.utils.auth import get_current_user

def login(func):
    @wraps(func)
    def sub_function(*args,**kwargs):
        user  = get_current_user()
        if not user:
            return {'Message':'Authentication required'},401
        
        return func(*args,user=user,**kwargs)
    return sub_function


def librarian(func):
    @wraps(func)
    def sub_function(user,*args,**kwargs):
        if user.user_role != 'librarian':
            return {'Message': 'Only librarian can access'},403
        return func(user,*args,**kwargs)
    return sub_function


        
