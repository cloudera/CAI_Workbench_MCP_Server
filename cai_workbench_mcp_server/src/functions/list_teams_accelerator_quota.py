"""List team accelerator quota (admin)."""

import requests
from typing import Any, Dict

from .http_helpers import auth_headers, normalize_host, pick_query, request_error

_Q = ("search_filter",)


def list_teams_accelerator_quota(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        host = normalize_host(config.get("host", ""))
        api_key = config.get("api_key")
        if not api_key:
            return {"success": False, "message": "Missing api_key in configuration"}
        q = pick_query(params or {}, _Q)
        r = requests.get(
            f"{host}/api/v2/userslabels/team-quota", headers=auth_headers(api_key), params=q, timeout=60
        )
        r.raise_for_status()
        return {"success": True, "message": "list_teams_accelerator_quota ok", "data": r.json()}
    except Exception as e:
        return request_error("list_teams_accelerator_quota", e)
