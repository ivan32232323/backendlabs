from __future__ import annotations

from flask_restful import Resource

from ..store import store, serialize
from .common import get_json


class UserCreateResource(Resource):
    def post(self):
        data = get_json()
        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            return {"message": "Field 'name' is required"}, 400
        user = store.create_user(name=name.strip())
        return serialize(user), 201


class UsersResource(Resource):
    def get(self):
        return [serialize(u) for u in store.list_users()], 200


class UserItemResource(Resource):
    def get(self, user_id: int):
        user = store.get_user(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return serialize(user), 200

    def delete(self, user_id: int):
        if store.delete_user(user_id):
            return {"message": "User deleted"}, 200
        return {"message": "User not found"}, 404
