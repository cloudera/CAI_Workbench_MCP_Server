"""Stop a job run in Cloudera AI."""

from typing import Any, Dict

try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception

from .http_helpers import setup_client, serialize_result


def stop_job_run(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Stop a running job run."""
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
        result = client.stop_job_run(project_id, job_id, run_id)
        return {
            "success": True,
            "message": f"Successfully stopped job run '{run_id}'",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error stopping job run: {str(e)}"}
