from __future__ import annotations

from flask import request


def get_json() -> dict:
    if not request.is_json:
        return {}
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}
