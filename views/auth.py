from flask_restx import Namespace, Resource
from flask import request
from implemented import auth_service
from views.users import user_schema

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):

    def post(self):
        return auth_service.login(request.json)


    def put(self):
        return auth_service.get_new_token(request.json['refresh_token'])
