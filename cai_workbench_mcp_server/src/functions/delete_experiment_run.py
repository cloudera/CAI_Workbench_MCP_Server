"""Delete an experiment run in Cloudera AI."""

from typing import Any, Dict

try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None

from .http_helpers import setup_client, serialize_result


def delete_experiment_run(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Delete an experiment run."""
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

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.delete_experiment_run(project_id, experiment_id, run_id)
        return {
            "success": True,
            "message": f"Successfully deleted experiment run '{run_id}'",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error deleting experiment run: {str(e)}"}
