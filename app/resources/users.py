from __future__ import annotations

from flask_jwt_extended import jwt_required
from flask_restful import Resource

from ..store import store, serialize
from .common import get_json


class RegisterResource(Resource):
    # POST /user
    def post(self):
        data = get_json()
        username = data.get("username")
        password = data.get("password")

        if not isinstance(username, str) or not username.strip():
            return {"message": "Field 'username' is required"}, 400
        if not isinstance(password, str) or len(password) < 4:
            return {"message": "Field 'password' is required (min 4 chars)"}, 400

        try:
            user = store.create_user(username=username.strip(), password_plain=password)
        except ValueError as e:
            if str(e) == "username_taken":
                return {"message": "Username already exists"}, 409
            raise

        return serialize(user), 201


class UsersResource(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        return [serialize(u) for u in store.list_users()], 200


class UserItemResource(Resource):
    method_decorators = [jwt_required()]

    def get(self, user_id: int):
        user = store.get_user(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return serialize(user), 200

    def delete(self, user_id: int):
        if store.delete_user(user_id):
            return {"message": "User deleted"}, 200
        return {"message": "User not found"}, 404
