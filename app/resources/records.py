from __future__ import annotations

from flask import request
from flask_restful import Resource

from ..store import store, serialize
from .common import get_json


class RecordItemResource(Resource):
    def get(self, record_id: int):
        record = store.get_record(record_id)
        if not record:
            return {"message": "Record not found"}, 404
        return serialize(record), 200

    def delete(self, record_id: int):
        if store.delete_record(record_id):
            return {"message": "Record deleted"}, 200
        return {"message": "Record not found"}, 404


class RecordCollectionResource(Resource):
    def post(self):
        data = get_json()
        user_id = data.get("user_id")
        category_id = data.get("category_id")
        amount = data.get("amount")

        try:
            user_id = int(user_id)
            category_id = int(category_id)
            amount = float(amount)
        except (TypeError, ValueError):
            return {"message": "user_id, category_id, amount are required"}, 400

        if not store.get_user(user_id):
            return {"message": "User not found"}, 404
        if not store.get_category(category_id):
            return {"message": "Category not found"}, 404

        record = store.create_record(user_id=user_id, category_id=category_id, amount=amount)
        return serialize(record), 201

    def get(self):
        # must accept user_id and/or category_id; without params => error
        user_id = request.args.get("user_id")
        category_id = request.args.get("category_id")

        if user_id is None and category_id is None:
            return {"message": "Provide at least one query param: user_id or category_id"}, 400

        user_id_int = None
        category_id_int = None
        try:
            if user_id is not None:
                user_id_int = int(user_id)
            if category_id is not None:
                category_id_int = int(category_id)
        except ValueError:
            return {"message": "user_id and category_id must be integers"}, 400

        records = store.filter_records(user_id=user_id_int, category_id=category_id_int)
        return [serialize(r) for r in records], 200
