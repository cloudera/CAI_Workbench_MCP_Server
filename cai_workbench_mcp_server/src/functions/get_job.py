"""Get job in Cloudera AI."""

from typing import Any, Dict

try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception

from .http_helpers import setup_client, serialize_result


def get_job(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Get job in Cloudera AI."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    job_id = params.get("job_id")
    if not job_id:
        return {"success": False, "message": "job_id is required"}

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.get_job(project_id, job_id)
        return {
            "success": True,
            "message": f"Successfully getd job",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
