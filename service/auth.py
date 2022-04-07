from dao.auth import AuthDAO


from utils import generate_tokens, decode_token





class AuthService:
    def __init__(self, dao: AuthDAO):
        self.dao = dao

    def login(self, username, password):


        user = self.dao.get_by_username(username)



        if user is None or not user.compare_password(password):
           return"no such user or wrong username and/or password"

        tokens: dict = generate_tokens({
                    'username': user.username,
                    'role': user.role
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
