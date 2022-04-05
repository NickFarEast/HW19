from dao.auth import AuthDAO
from flask_restx import abort

from dao.model.user import UserSchema
from utils import get_hash_password, generate_tokens
import json
users_schema = UserSchema(many=True)

class AuthService:
    def __init__(self, dao: AuthDAO):
        self.dao = dao

    def login(self, data: dict):
        print(data)

        users_data = self.dao.get_by_username(data['username'])
        if users_data is None:
            abort(401, message='User not found')

        users = users_schema.dumps(users_data)
        user_dict = json.loads(users)
        password = data['password']
        hashed_password = get_hash_password(password=password)

        for user in user_dict:
            if user['password'] == hashed_password:

                tokens: dict = generate_tokens({
                               'username': data['username'],
                               'role': user['role']
                 }, )

                return tokens


