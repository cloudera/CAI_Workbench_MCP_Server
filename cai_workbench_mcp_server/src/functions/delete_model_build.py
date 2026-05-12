"""Delete a model build in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

def delete_model_build(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Delete a model build."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    model_id = params.get("model_id")
    build_id = params.get("build_id")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not model_id:
        return {"success": False, "message": "model_id is required"}
    if not build_id:
        return {"success": False, "message": "build_id is required"}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.delete_model_build(project_id, model_id, build_id)
        return {"success": True, "message": f"Successfully deleted model build '{build_id}'", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
