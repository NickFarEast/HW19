from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service

from flask import request

from utils import auth_required

director_ns = Namespace('directors')


director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        """Функция для отображения всех режиссеров в базе"""
        all_directors = director_service.get_all()

        return directors_schema.dumps(all_directors), 200

    def post(self):
        """Функция для записи нового режиссера в базу"""
        req_jason = director_schema.load(request.json)
        director_service.create(req_jason)

        return "", 201


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    @auth_required
    def get(self, did):
        """Функция для получения режиссера из базы по ID"""
        director = director_service.get_one(did)
        return director_schema.dump(director), 200


    def put(self, did):
        """Функция для внесения изменения в базу по ID"""
        req_jason = director_schema.load(request.json)
        req_jason["id"] = did

        director_service.update(req_jason)

        return "", 204

    def delete(self, did):
        """Функция для удаления из базы по ID"""
        director_service.delete(did)
        return "", 204