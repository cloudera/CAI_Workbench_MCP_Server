"""Cloudera AI: validate_api_key."""

import json
from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception
from .http_helpers import setup_client, serialize_result

def validate_api_key(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """validate_api_key."""
    params = params or {}
    body_json = params.get("body_json")
    if not body_json:
        return {"success": False, "message": "body_json is required"}
    body = json.loads(body_json) if isinstance(body_json, str) else body_json
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.validate_api_key(body)
        return {"success": True, "message": "validate_api_key ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
