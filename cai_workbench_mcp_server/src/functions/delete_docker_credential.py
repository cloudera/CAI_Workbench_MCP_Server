"""Delete a Docker credential."""

import requests
from typing import Any, Dict

from .http_helpers import auth_headers, normalize_host, request_error


def delete_docker_credential(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        cid = params.get("docker_credential_id")
        if not cid:
            return {"success": False, "message": "Missing docker_credential_id"}
        host = normalize_host(config.get("host", ""))
        api_key = config.get("api_key")
        if not api_key:
            return {"success": False, "message": "Missing api_key in configuration"}
        r = requests.delete(
            f"{host}/api/v2/dockercredentials/{cid}",
            headers=auth_headers(api_key),
            timeout=60,
        )
        r.raise_for_status()
        try:
            data = r.json() if r.text else {}
        except Exception:
            data = {"raw": r.text}
        return {"success": True, "message": "delete_docker_credential ok", "data": data}
    except Exception as e:
        return request_error("delete_docker_credential", e)
