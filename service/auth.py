from dao.auth import AuthDAO
from flask_restx import abort

from dao.model.user import UserSchema
from utils import get_hash_password, generate_tokens, decode_token
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

    def get_new_token(self, refresh_token: str):
        decoded_token = decode_token(refresh_token, refresh_token=True)

        tokens = generate_tokens(
            data={
                'username': decoded_token['username'],
                'role': decoded_token['role'],
            },
        )

        return tokens
