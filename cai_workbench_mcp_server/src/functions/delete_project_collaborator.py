"""Delete a project collaborator in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception
from .http_helpers import setup_client, serialize_result

def delete_project_collaborator(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Remove a collaborator from a project."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    username = params.get("username")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not username:
        return {"success": False, "message": "username is required"}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.delete_project_collaborator(project_id, username)
        return {"success": True, "message": f"Successfully removed collaborator '{username}'", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
