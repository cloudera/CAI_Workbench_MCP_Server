"""Delete an API v2 key in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception
from .http_helpers import setup_client, serialize_result

def delete_v2_key(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Delete one API v2 key."""
    params = params or {}
    username = params.get("username")
    key_id = params.get("key_id")
    if not username:
        return {"success": False, "message": "username is required"}
    if not key_id:
        return {"success": False, "message": "key_id is required"}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.delete_v2_key(username, key_id)
        return {"success": True, "message": f"Successfully deleted key '{key_id}'", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
