from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
from app.models import *
migrate = Migrate()

authorizations = {
    'Bearer Token' : {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description':'Paste your token here: Bearer ######;'
    }
}


api = Api(
    title="Library  Management API",
    version="1.0",
    description="Library Management Flask based API with JWT Token",
    authorizations=authorizations,
    security='Bearer Token'
)

limiter = Limiter(
        app=None,
        key_func=get_remote_address,
        default_limits=["200 per day","50 per hour"]
    )
    


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    migrate.init_app(app,db)
    api.init_app(app)
    limiter.init_app(app)
    

    from app.urls.book_url import book_ns
    from app.urls.auth_url import auth_ns
    from app.urls.borrow_url import borrow_ns
    api.add_namespace(book_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(borrow_ns)

    with app.app_context():
        from flask_migrate import upgrade
        try:
            upgrade()
            print('database upgraded successfully')
        except Exception as e:
            print('upgrade failed:{e}')




    return app

