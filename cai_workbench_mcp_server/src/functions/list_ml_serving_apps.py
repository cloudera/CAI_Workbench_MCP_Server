"""List ML serving apps in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

def list_ml_serving_apps(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """List ML serving apps."""
    params = params or {}
    kwargs = {}
    if params.get("force_refresh") is not None:
        kwargs["force_refresh"] = params["force_refresh"]
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.list_ml_serving_apps(**kwargs)
        return {"success": True, "message": "list_ml_serving_apps ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
