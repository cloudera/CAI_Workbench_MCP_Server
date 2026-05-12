"""List project collaborators in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

def list_project_collaborators(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """List collaborators of a project."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    kwargs = {}
    for k in ("search_filter", "page_size", "page_token", "sort"):
        if params.get(k):
            kwargs[k] = params[k]
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.list_project_collaborators(project_id, **kwargs)
        return {"success": True, "message": "list_project_collaborators ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
