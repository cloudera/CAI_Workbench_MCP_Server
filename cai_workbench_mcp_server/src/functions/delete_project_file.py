"""Delete a project file in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

def delete_project_file(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Delete a file from a project."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    file_path = params.get("file_path")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not file_path:
        return {"success": False, "message": "file_path is required"}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.delete_project_file(project_id, file_path)
        return {"success": True, "message": f"Successfully deleted file '{file_path}'", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
