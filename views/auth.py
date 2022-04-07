from flask_restx import Namespace, Resource
from flask import request
from implemented import auth_service
from views.users import user_schema

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):

    def post(self):
        req_json = request.json
        username = req_json.get('username')
        password = req_json.get('password')

        if None in [username, password]:
            return "", 400

        token = auth_service.login(username,password)

        return token

    def put(self):
        return auth_service.get_new_token(request.json['refresh_token'])
