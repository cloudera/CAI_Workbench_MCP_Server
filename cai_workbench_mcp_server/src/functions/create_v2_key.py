"""Create an API v2 key for a user."""

import requests
from typing import Any, Dict

from .http_helpers import auth_headers, normalize_host, request_error


def create_v2_key(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        user = params.get("username")
        if not user or not params.get("body"):
            return {"success": False, "message": "Missing username or body"}
        host = normalize_host(config.get("host", ""))
        api_key = config.get("api_key")
        if not api_key:
            return {"success": False, "message": "Missing api_key in configuration"}
        from urllib.parse import quote

        r = requests.post(
            f"{host}/api/v2/users/{quote(user, safe='')}/v2_keys",
            headers=auth_headers(api_key),
            json=params["body"],
            timeout=120,
        )
        r.raise_for_status()
        return {"success": True, "message": "create_v2_key ok", "data": r.json()}
    except Exception as e:
        return request_error("create_v2_key", e)
