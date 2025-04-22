import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS =  False
    SECRET_KEY = os.getenv('SECRET_KEY')

    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    RATELIMIT_STORAGE_URI = REDIS_URL 
    RATELIMIT_STRATEGY = "fixed-window"
    

# import secrets
# print(secrets.token_urlsafe(32))