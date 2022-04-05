from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service

from flask import request

user_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UserView(Resource):
    def get(self):
        """Функция для отображения всех пользователей в базе"""
        all_users = user_service.get_all()

        return users_schema.dumps(all_users), 200

    def post(self):
        """Функция для записи нового user в базу"""
        req_jason = user_schema.load(request.json)
        user_service.register(req_jason)

        return "", 201


@user_ns.route('/<uid>')
class UserView(Resource):

    def delete(self, uid):
        """Функция для удаления из базы по ID"""
        user_service.delete(uid)
        return "", 204
