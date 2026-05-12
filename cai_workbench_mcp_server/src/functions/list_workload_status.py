"""Cloudera AI: list_workload_status."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

def list_workload_status(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """list_workload_status."""
    params = params or {}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.list_workload_status()
        return {"success": True, "message": "list_workload_status ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
