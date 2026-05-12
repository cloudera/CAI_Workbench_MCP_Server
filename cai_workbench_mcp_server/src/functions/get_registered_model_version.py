"""Get a registered model version in Cloudera AI."""

from typing import Any, Dict
from cmlapi.rest import ApiException
from .http_helpers import setup_client, serialize_result

def get_registered_model_version(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Get registered model version details."""
    params = params or {}
    model_id = params.get("model_id")
    version_id = params.get("version_id")
    if not model_id:
        return {"success": False, "message": "model_id is required"}
    if not version_id:
        return {"success": False, "message": "version_id is required"}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.get_registered_model_version(model_id, version_id)
        return {"success": True, "message": "Successfully retrieved model version", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
