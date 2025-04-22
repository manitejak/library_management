from flask_restx import Namespace, Resource,fields
from flask import request
from app.views.auth_view import *

auth_ns = Namespace('auth', description='User AUthenticaltion')

registation_model = auth_ns.model('User Registration',{
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'email_id': fields.String(required=True),
    'user_role': fields.String(default='user',enum=['user','librarian'])

})

login_model = auth_ns.model('Login',{
    'username': fields.String(required=True),
    'password': fields.String(required=True)

})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(registation_model)
    def post(self):
        return register_user(request.json)
    

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        return login_user(request.json)
    
