"""Delete experiment runs in batch in Cloudera AI."""

from typing import Any, Dict

try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None

from .http_helpers import setup_client, serialize_result


def delete_experiment_run_batch(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Delete multiple experiment runs in a single request."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    experiment_id = params.get("experiment_id")
    run_ids = params.get("run_ids")

    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not experiment_id:
        return {"success": False, "message": "experiment_id is required"}
    if not run_ids:
        return {"success": False, "message": "run_ids is required"}

    ids_list = run_ids.split(",") if isinstance(run_ids, str) else run_ids
    body = {"run_ids": ids_list}

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.delete_experiment_run_batch(body, project_id, experiment_id)
        return {
            "success": True,
            "message": f"Successfully deleted {len(ids_list)} experiment runs",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error deleting experiment runs: {str(e)}"}
