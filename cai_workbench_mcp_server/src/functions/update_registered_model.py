"""Update a registered model in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception
from .http_helpers import setup_client, serialize_result

def update_registered_model(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Update a registered model."""
    params = params or {}
    model_id = params.get("model_id")
    if not model_id:
        return {"success": False, "message": "model_id is required"}
    body = {}
    if params.get("description"):
        body["description"] = params["description"]
    if params.get("visibility"):
        body["visibility"] = params["visibility"]
    if params.get("user_id"):
        body["user_id"] = params["user_id"]
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.update_registered_model(body, model_id)
        return {"success": True, "message": f"Successfully updated registered model '{model_id}'", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
