"""Cloudera AI: register_custom_runtime."""

import json
from typing import Any, Dict
from cmlapi.rest import ApiException
from .http_helpers import setup_client, serialize_result

def register_custom_runtime(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """register_custom_runtime."""
    params = params or {}
    body_json = params.get("body_json")
    if not body_json:
        return {"success": False, "message": "body_json is required"}
    body = json.loads(body_json) if isinstance(body_json, str) else body_json
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.register_custom_runtime(body)
        return {"success": True, "message": "register_custom_runtime ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
