import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS =  False
    SECRET_KEY = os.getenv('SECRET_KEY')
    

# import secrets
# print(secrets.token_urlsafe(32))