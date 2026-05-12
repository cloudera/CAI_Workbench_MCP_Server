"""Cloudera AI: list_all_accelerator_node_labels."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

def list_all_accelerator_node_labels(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """list_all_accelerator_node_labels."""
    params = params or {}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.list_all_accelerator_node_labels()
        return {"success": True, "message": "list_all_accelerator_node_labels ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
