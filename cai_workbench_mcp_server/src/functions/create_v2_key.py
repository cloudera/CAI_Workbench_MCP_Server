"""Create an API v2 key in Cloudera AI."""

import json
from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception
from .http_helpers import setup_client, serialize_result

def create_v2_key(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Create API v2 key."""
    params = params or {}
    username = params.get("username")
    body_json = params.get("body_json")
    if not username:
        return {"success": False, "message": "username is required"}
    if not body_json:
        return {"success": False, "message": "body_json is required"}
    body = json.loads(body_json) if isinstance(body_json, str) else body_json
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.create_v2_key(body, username)
        return {"success": True, "message": "create_v2_key ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
