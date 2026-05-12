"""Update an experiment run in Cloudera AI."""

import json
from typing import Any, Dict

try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None

from .http_helpers import setup_client, serialize_result


def update_experiment_run(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Update an experiment run."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    experiment_id = params.get("experiment_id")
    run_id = params.get("run_id")

    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not experiment_id:
        return {"success": False, "message": "experiment_id is required"}
    if not run_id:
        return {"success": False, "message": "run_id is required"}

    body = {}
    if params.get("name"):
        body["name"] = params["name"]
    if params.get("description"):
        body["description"] = params["description"]
    if params.get("metrics"):
        body["metrics"] = json.loads(params["metrics"]) if isinstance(params["metrics"], str) else params["metrics"]
    if params.get("parameters"):
        body["parameters"] = json.loads(params["parameters"]) if isinstance(params["parameters"], str) else params["parameters"]
    if params.get("tags"):
        body["tags"] = params["tags"].split(",") if isinstance(params["tags"], str) else params["tags"]

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.update_experiment_run(body, project_id, experiment_id, run_id)
        return {
            "success": True,
            "message": f"Successfully updated experiment run '{run_id}'",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error updating experiment run: {str(e)}"}
