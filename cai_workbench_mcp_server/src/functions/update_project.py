"""Update a project in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

def update_project(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Update a project."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    body = {}
    for key in ("name", "summary", "template"):
        if params.get(key):
            body[key] = params[key]
    if params.get("public") is not None:
        body["public"] = params["public"]
    if params.get("disable_git_repo") is not None:
        body["disable_git_repo"] = params["disable_git_repo"]
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.update_project(body, project_id)
        return {"success": True, "message": f"Successfully updated project '{project_id}'", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
