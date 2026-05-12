"""Create an experiment in Cloudera AI."""

from typing import Any, Dict

from cmlapi.rest import ApiException

from .http_helpers import setup_client, serialize_result


def create_experiment(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new experiment in a Cloudera AI project."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not params.get("name"):
        return {"success": False, "message": "name is required"}

    body = {"name": params["name"]}
    if params.get("description"):
        body["description"] = params["description"]

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.create_experiment(body, project_id)
        return {
            "success": True,
            "message": f"Successfully created experiment",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error creating experiment: {str(e)}"}
