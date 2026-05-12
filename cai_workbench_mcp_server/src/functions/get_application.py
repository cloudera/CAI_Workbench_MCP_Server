"""Get an application in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

def get_application(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Get application details."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    application_id = params.get("application_id")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not application_id:
        return {"success": False, "message": "application_id is required"}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.get_application(project_id, application_id)
        return {"success": True, "message": f"Successfully retrieved application '{application_id}'", "application_id": application_id, "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
