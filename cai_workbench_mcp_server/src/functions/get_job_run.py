"""Get a job run in Cloudera AI."""

from typing import Any, Dict

try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None

from .http_helpers import setup_client, serialize_result


def get_job_run(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Get details of a job run."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    job_id = params.get("job_id")
    run_id = params.get("run_id")

    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not job_id:
        return {"success": False, "message": "job_id is required"}
    if not run_id:
        return {"success": False, "message": "run_id is required"}

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.get_job_run(project_id, job_id, run_id)
        return {
            "success": True,
            "message": "Successfully retrieved job run",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error getting job run: {str(e)}"}
