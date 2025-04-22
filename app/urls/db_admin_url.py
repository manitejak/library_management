from flask_restx import Namespace, Resource
from flask_migrate import init, migrate, upgrade, stamp
from flask import jsonify
from app import db

db_admin_ns = Namespace('db-admin', description='Database administration operations')

@db_admin_ns.route('/init')
class DBInit(Resource):
    def post(self):
        try:
            db.create_all()
            init()  # Initialize migrations
            return {'message': 'Database initialized successfully.'}, 201
        except Exception as e:
            return {'error': str(e)}, 500

@db_admin_ns.route('/migrate')
class DBMigrate(Resource):
    def post(self):
        try:
            migrate()
            stamp()
            return {'message': 'Migration script created and database stamped.'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

@db_admin_ns.route('/upgrade')
class DBUpgrade(Resource):
    def post(self):
        try:
            upgrade()
            return {'message': 'Database upgraded successfully.'}, 200
        except Exception as e:
            return {'error': str(e)}, 500
