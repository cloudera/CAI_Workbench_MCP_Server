"""Create a model in Cloudera AI."""

from typing import Any, Dict

from cmlapi.rest import ApiException

from .http_helpers import setup_client, serialize_result


def create_model(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new model."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not params.get("name"):
        return {"success": False, "message": "name is required"}

    body = {"name": params["name"]}
    if params.get("description"):
        body["description"] = params["description"]
    if params.get("disable_authentication") is not None:
        body["disable_authentication"] = params["disable_authentication"]

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.create_model(body, project_id)
        return {"success": True, "message": "Successfully created model", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
