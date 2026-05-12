"""Get default quota in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception
from .http_helpers import setup_client, serialize_result

def get_default_quota(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Get default user quota."""
    params = params or {}
    kwargs = {}
    if params.get("uuid"):
        kwargs["uuid"] = params["uuid"]
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.get_default_quota(**kwargs)
        return {"success": True, "message": "get_default_quota ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
