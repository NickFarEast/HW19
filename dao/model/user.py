from marshmallow import Schema, fields

from setup_db import db
from utils import get_hash_password


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

    def compare_password(self, other_password) -> bool:
        hashed_password = get_hash_password(other_password)
        return hashed_password == self.password




class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str()
    role = fields.Str()
