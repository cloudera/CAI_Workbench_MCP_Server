"""List resource groups."""

import requests
from typing import Any, Dict

from .http_helpers import auth_headers, normalize_host, request_error


def list_all_resource_groups(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        host = normalize_host(config.get("host", ""))
        api_key = config.get("api_key")
        if not api_key:
            return {"success": False, "message": "Missing api_key in configuration"}
        r = requests.get(f"{host}/api/v2/resourcegroups", headers=auth_headers(api_key), timeout=60)
        r.raise_for_status()
        return {"success": True, "message": "list_all_resource_groups ok", "data": r.json()}
    except Exception as e:
        return request_error("list_all_resource_groups", e)
