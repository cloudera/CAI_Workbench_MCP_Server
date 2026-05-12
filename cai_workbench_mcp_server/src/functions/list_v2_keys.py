"""List API v2 keys in Cloudera AI."""

from typing import Any, Dict
from cmlapi.rest import ApiException
from .http_helpers import setup_client, serialize_result

def list_v2_keys(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """List API v2 keys for a user."""
    params = params or {}
    username = params.get("username")
    if not username:
        return {"success": False, "message": "username is required"}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.list_v2_keys(username)
        return {"success": True, "message": "list_v2_keys ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
