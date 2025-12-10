from __future__ import annotations

from flask import request
from flask_restful import Resource

from ..store import store, serialize
from .common import get_json


class CategoryResource(Resource):
    def get(self):
        return [serialize(c) for c in store.list_categories()], 200

    def post(self):
        data = get_json()
        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            return {"message": "Field 'name' is required"}, 400
        category = store.create_category(name=name.strip())
        return serialize(category), 201

    def delete(self):
        # Spec doesn't include <id> in path, so accept ?category_id=... or JSON {"id": ...}
        category_id = request.args.get("category_id")
        if category_id is None:
            data = get_json()
            category_id = data.get("id")
        try:
            category_id_int = int(category_id)
        except (TypeError, ValueError):
            return {"message": "category_id (query) or id (json) is required"}, 400

        if store.delete_category(category_id_int):
            return {"message": "Category deleted"}, 200
        return {"message": "Category not found"}, 404
