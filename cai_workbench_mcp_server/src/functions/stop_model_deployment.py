"""Stop a model deployment in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception
from .http_helpers import setup_client, serialize_result

def stop_model_deployment(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Stop a model deployment."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    model_id = params.get("model_id")
    deployment_id = params.get("deployment_id")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not model_id:
        return {"success": False, "message": "model_id is required"}
    if not deployment_id:
        return {"success": False, "message": "deployment_id is required"}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.stop_model_deployment(project_id, model_id, deployment_id)
        return {"success": True, "message": f"Successfully stopped deployment '{deployment_id}'", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
