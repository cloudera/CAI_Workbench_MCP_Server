"""List applications in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

def list_applications(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """List applications in a project."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.list_applications(project_id)
        data = serialize_result(result)
        apps = data.get("applications", []) if data else []
        return {"success": True, "message": f"Found {len(apps)} applications", "applications": apps, "count": len(apps)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
