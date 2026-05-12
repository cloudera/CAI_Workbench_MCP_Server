"""List project files in Cloudera AI."""

from typing import Any, Dict
from cmlapi.rest import ApiException
from .http_helpers import setup_client, serialize_result

def list_project_files(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """List files in a project."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    path = params.get("path", "")
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.list_project_files(project_id, path)
        return {"success": True, "message": "list_project_files ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
