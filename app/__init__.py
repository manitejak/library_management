from flask import Flask,jsonify,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from config import Config
from flask_swagger_ui import get_swaggerui_blueprint

# Initialize SQLAlchemy instance
db = SQLAlchemy()
# Initialize Flask-Migrate for database migrations
migrate = Migrate()

# Import models after db initialization to avoid circular imports
from app.models import *


# Authorization configuration for Swagger documentation
authorizations = {
    'Bearer Token' : {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description':'Paste your token here: Bearer ######;'
    }
}

# Initialize the Flask-RESTx API with documentation metadata
api = Api(
    title="Library  Management API",
    version="1.0",
    description="Library Management Flask based API with JWT Token",
    authorizations=authorizations,
    security='Bearer Token'
)


def create_app():
    """Factory function to create and configure the Flask application.
    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    
    
    # Swagger UI configuration
    SWAGGER_URL = '/swagger'
    API_URL = '/swagger.json'
    # Create Swagger UI blueprint
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name':'Library management system API'
        }
    )

    app.register_blueprint(swagger_ui_blueprint,url_prefix=SWAGGER_URL)

    api.init_app(app)

    @app.route('/swagger.json')
    def swagger_json():
        return jsonify(api.__schema__)
    
    @app.route('/')
    def index():
        return redirect('/swagger/')

    # Register namespaces
    from app.urls.book_url import book_ns
    from app.urls.auth_url import auth_ns
    from app.urls.borrow_url import borrow_ns
    api.add_namespace(book_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(borrow_ns)

    
   # Database initialization
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f'Database initialization failed: {e}')

    return app

