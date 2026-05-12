"""Delete all API v2 keys in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

def delete_v2_keys(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Delete all API v2 keys for a user."""
    params = params or {}
    username = params.get("username")
    if not username:
        return {"success": False, "message": "username is required"}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.delete_v2_keys(username)
        return {"success": True, "message": f"Successfully deleted all keys for '{username}'", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
