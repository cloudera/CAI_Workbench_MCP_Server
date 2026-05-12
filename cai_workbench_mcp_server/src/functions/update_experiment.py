"""Update an experiment in Cloudera AI."""

from typing import Any, Dict

try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception

from .http_helpers import setup_client, serialize_result


def update_experiment(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Update an experiment."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    experiment_id = params.get("experiment_id")

    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not experiment_id:
        return {"success": False, "message": "experiment_id is required"}

    body = {}
    if params.get("name"):
        body["name"] = params["name"]
    if params.get("description"):
        body["description"] = params["description"]

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.update_experiment(body, project_id, experiment_id)
        return {
            "success": True,
            "message": f"Successfully updated experiment '{experiment_id}'",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error updating experiment: {str(e)}"}
