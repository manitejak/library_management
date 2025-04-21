from flask import request
from app.models import User
from app import db
import jwt as pyjwt
import datetime
from functools import wraps
from config import Config
from app.models import User

def encode_jwt(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.user_role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        
    }
    return pyjwt.encode(payload,Config.SECRET_KEY, algorithm='HS256')

def decode_jwt(token):
    try:
        data = pyjwt.decode(token,Config.SECRET_KEY, algorithms = ['HS256'])
        return data
    except pyjwt.ExpiredSignatureError:
        return None
    except pyjwt.InvalidTokenError:
        return None
    


def get_current_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    print(token)
    data = decode_jwt(token)
    print(data)
    if not data:
        return None
    return User.query.get(data['user_id'])




