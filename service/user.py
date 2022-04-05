from dao.user import UserDAO
from utils import get_hash_password


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def register(self, data):
        data["password"] = get_hash_password(data.get("password"))
        return self.dao.create(data)



    def delete(self, rid):
        self.dao.delete(rid)



