from __future__ import annotations

from flask_jwt_extended import create_access_token
from flask_restful import Resource

from ..store import store
from .common import get_json


class LoginResource(Resource):
    # POST /login
    def post(self):
        data = get_json()
        username = data.get("username")
        password = data.get("password")

        if not isinstance(username, str) or not username.strip():
            return {"message": "Field 'username' is required"}, 400
        if not isinstance(password, str):
            return {"message": "Field 'password' is required"}, 400

        user = store.get_user_by_username(username.strip())
        if user and store.verify_password(user, password):
            # PyJWT expects sub (identity) to be a string
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token, "user_id": user.id}, 200

        return {"message": "Bad username or password"}, 401
