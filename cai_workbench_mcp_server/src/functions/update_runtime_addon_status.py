"""Update runtime addon status."""

import requests
from typing import Any, Dict

from .http_helpers import auth_headers, normalize_host, request_error


def update_runtime_addon_status(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if not params.get("body"):
            return {"success": False, "message": "Missing body (UpdateRuntimeAddonStatusRequest)"}
        host = normalize_host(config.get("host", ""))
        api_key = config.get("api_key")
        if not api_key:
            return {"success": False, "message": "Missing api_key in configuration"}
        r = requests.post(
            f"{host}/api/v2/runtimeaddons:updatestatus",
            headers=auth_headers(api_key),
            json=params["body"],
            timeout=120,
        )
        r.raise_for_status()
        return {"success": True, "message": "update_runtime_addon_status ok", "data": r.json()}
    except Exception as e:
        return request_error("update_runtime_addon_status", e)
