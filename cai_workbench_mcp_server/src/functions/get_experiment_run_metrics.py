"""Get experiment run metrics in Cloudera AI."""

from typing import Any, Dict

from cmlapi.rest import ApiException

from .http_helpers import setup_client, serialize_result


def get_experiment_run_metrics(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Get metrics for an experiment run."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    experiment_id = params.get("experiment_id")
    run_id = params.get("run_id")
    metric_key = params.get("metric_key")

    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not experiment_id:
        return {"success": False, "message": "experiment_id is required"}
    if not run_id:
        return {"success": False, "message": "run_id is required"}
    if not metric_key:
        return {"success": False, "message": "metric_key is required"}

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.get_experiment_run_metrics(project_id, experiment_id, run_id, metric_key)
        return {
            "success": True,
            "message": "Successfully retrieved experiment run metrics",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error getting metrics: {str(e)}"}
