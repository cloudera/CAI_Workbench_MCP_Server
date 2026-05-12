"""Update a registered model version in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception
from .http_helpers import setup_client, serialize_result

def update_registered_model_version(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Update a registered model version."""
    params = params or {}
    model_id = params.get("model_id")
    model_version_id = params.get("model_version_id")
    if not model_id:
        return {"success": False, "message": "model_id is required"}
    if not model_version_id:
        return {"success": False, "message": "model_version_id is required"}
    body = {}
    if params.get("notes"):
        body["notes"] = params["notes"]
    if params.get("tags"):
        body["tags"] = params["tags"].split(",") if isinstance(params["tags"], str) else params["tags"]
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.update_registered_model_version(body, model_id, model_version_id)
        return {"success": True, "message": f"Successfully updated model version '{model_version_id}'", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
