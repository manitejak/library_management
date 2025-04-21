import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL','postgresql://teja:teja@localhost/library')
    SQLALCHEMY_TRACK_MODIFICATIONS =  False
    SECRET_KEY = 'HpbMJZuFcNmbT6utOWtUPKZw_fZbC-32TrG1GT4BY5g'
    

# import secrets
# print(secrets.token_urlsafe(32))