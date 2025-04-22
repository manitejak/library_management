from flask import Flask,jsonify,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from config import Config
from flask_swagger_ui import get_swaggerui_blueprint

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


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    api.init_app(app)
    
    SWAGGER_URL = '/swagger'
    API_URL = '/swagger.json'

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name':'Library management system API'
        }
    )

    app.register_blueprint(swagger_ui_blueprint,url_prefix=SWAGGER_URL)

    @app.route('/swagger.json')
    def swagger_json():
        return jsonify(api.__schema__)


    from app.urls.book_url import book_ns
    from app.urls.auth_url import auth_ns
    from app.urls.borrow_url import borrow_ns
    api.add_namespace(book_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(borrow_ns)

    with app.app_context():
        try:
            from flask_migrate import upgrade
            db.create_all()
            upgrade()
            print('database upgraded successfully')
        except Exception as e:
            print('upgrade failed:',{e})

    @app.route('/')
    def index():
        return redirect('/swagger')

    return app

