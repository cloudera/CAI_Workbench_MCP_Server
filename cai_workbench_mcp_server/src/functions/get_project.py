"""Get a project in Cloudera AI."""

from typing import Any, Dict
from cmlapi.rest import ApiException
from .http_helpers import setup_client, serialize_result

def get_project(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Get project details."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.get_project(project_id)
        return {"success": True, "message": "Successfully retrieved project", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
