from __future__ import annotations

from flask_restful import Api

from .users import UserItemResource, UsersResource, UserCreateResource
from .categories import CategoryResource
from .records import RecordItemResource, RecordCollectionResource


def register_routes(api: Api) -> None:
    # Users
    api.add_resource(UserItemResource, "/user/<int:user_id>")
    api.add_resource(UsersResource, "/users")
    api.add_resource(UserCreateResource, "/user")

    # Categories (GET/POST/DELETE on /category)
    api.add_resource(CategoryResource, "/category")

    # Records
    api.add_resource(RecordItemResource, "/record/<int:record_id>")
    api.add_resource(RecordCollectionResource, "/record")
