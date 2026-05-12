"""Add a project collaborator in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception
from .http_helpers import setup_client, serialize_result

def add_project_collaborator(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Add a collaborator to a project."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not params.get("username"):
        return {"success": False, "message": "username is required"}
    if not params.get("permission"):
        return {"success": False, "message": "permission is required"}
    body = {"username": params["username"], "permission": params["permission"]}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.add_project_collaborator(body, project_id)
        return {"success": True, "message": f"Successfully added collaborator '{params['username']}'", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
