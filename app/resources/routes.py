from __future__ import annotations

from flask_restful import Api

from .auth import LoginResource
from .users import UserItemResource, UsersResource, RegisterResource
from .categories import CategoryResource
from .records import RecordItemResource, RecordCollectionResource


def register_routes(api: Api) -> None:
    # Auth
    api.add_resource(LoginResource, "/login")

    # Users
    api.add_resource(UserItemResource, "/user/<int:user_id>")
    api.add_resource(UsersResource, "/users")
    api.add_resource(RegisterResource, "/user")  # registration (replaces simple create from lab2)

    # Categories (GET/POST/DELETE on /category)
    api.add_resource(CategoryResource, "/category")

    # Records
    api.add_resource(RecordItemResource, "/record/<int:record_id>")
    api.add_resource(RecordCollectionResource, "/record")
