"""Delete all API v2 keys for a user."""

import requests
from typing import Any, Dict

from .http_helpers import auth_headers, normalize_host, request_error


def delete_v2_keys(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        user = params.get("username")
        if not user:
            return {"success": False, "message": "Missing username"}
        host = normalize_host(config.get("host", ""))
        api_key = config.get("api_key")
        if not api_key:
            return {"success": False, "message": "Missing api_key in configuration"}
        from urllib.parse import quote

        r = requests.delete(
            f"{host}/api/v2/users/{quote(user, safe='')}/v2_keys",
            headers=auth_headers(api_key),
            timeout=60,
        )
        r.raise_for_status()
        try:
            data = r.json() if r.text else {}
        except Exception:
            data = {"raw": r.text}
        return {"success": True, "message": "delete_v2_keys ok", "data": data}
    except Exception as e:
        return request_error("delete_v2_keys", e)
