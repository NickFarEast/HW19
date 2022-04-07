from dao.model.user import User


class AuthDAO:
    def __init__(self, session):
        self.session = session

    def get_by_username(self, data):
        return self.session.query(User).filter(User.username == data).first()
