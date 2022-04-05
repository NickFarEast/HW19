from flask_restx import Namespace, Resource
from flask import request
from implemented import auth_service
from views.users import user_schema

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):

    def post(self):
        print(type(request.json))
        return auth_service.login(request.json)