"""Log experiment run metrics/params in batch in Cloudera AI."""

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


def log_experiment_run_batch(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Log metrics and parameters for multiple experiment runs in batch."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    experiment_id = params.get("experiment_id")
    run_updates = params.get("run_updates")

    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not experiment_id:
        return {"success": False, "message": "experiment_id is required"}
    if not run_updates:
        return {"success": False, "message": "run_updates is required"}

    body = json.loads(run_updates) if isinstance(run_updates, str) else run_updates

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.log_experiment_run_batch(body, project_id, experiment_id)
        return {
            "success": True,
            "message": "Successfully logged experiment run batch",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error logging batch: {str(e)}"}
