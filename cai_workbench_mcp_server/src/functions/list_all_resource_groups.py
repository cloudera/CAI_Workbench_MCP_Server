"""Cloudera AI: list_all_resource_groups."""

from typing import Any, Dict
from cmlapi.rest import ApiException
from .http_helpers import setup_client, serialize_result

def list_all_resource_groups(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """list_all_resource_groups."""
    params = params or {}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.list_all_resource_groups()
        return {"success": True, "message": "list_all_resource_groups ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
