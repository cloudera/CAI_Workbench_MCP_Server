"""Download a project file in Cloudera AI."""

from typing import Any, Dict
from cmlapi.rest import ApiException
from .http_helpers import setup_client

def download_project_file(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Download a file from a project."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    path = params.get("path")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not path:
        return {"success": False, "message": "path is required"}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.download_project_file(project_id, path)
        content = result if isinstance(result, str) else str(result)
        return {"success": True, "message": f"Successfully downloaded '{path}'", "data": {"content": content, "path": path}}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
