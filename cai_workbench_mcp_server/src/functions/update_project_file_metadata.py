"""Update project file metadata in Cloudera AI."""

from typing import Any, Dict
from cmlapi.rest import ApiException
from .http_helpers import setup_client, serialize_result

def update_project_file_metadata(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Update metadata of a project file."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    file_path = params.get("file_path")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not file_path:
        return {"success": False, "message": "file_path is required"}
    body = {}
    if params.get("description"):
        body["description"] = params["description"]
    if params.get("hidden") is not None:
        body["hidden"] = params["hidden"]
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.update_project_file_metadata(body, project_id, file_path)
        return {"success": True, "message": f"Successfully updated file metadata for '{file_path}'", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
