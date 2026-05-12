"""Delete all jobs in a Cloudera AI project."""

from typing import Any, Dict

try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None

from .http_helpers import setup_client, serialize_result


def delete_all_jobs(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Delete all jobs in a project."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")

    if not project_id:
        return {"success": False, "message": "project_id is required"}

    try:
        client = setup_client(config["host"], config["api_key"])
        jobs_result = client.list_jobs(project_id)
        jobs_data = jobs_result.to_dict() if hasattr(jobs_result, "to_dict") else jobs_result
        jobs = jobs_data.get("jobs", [])

        if not jobs:
            return {"success": True, "message": "No jobs found to delete", "data": {"deleted": 0}}

        deleted = []
        failed = []
        for job in jobs:
            job_id = job.get("id")
            try:
                client.delete_job(project_id, job_id)
                deleted.append(job_id)
            except Exception as e:
                failed.append({"id": job_id, "error": str(e)})

        return {
            "success": True,
            "message": f"Deleted {len(deleted)} jobs, {len(failed)} failed",
            "data": {"deleted": len(deleted), "failed": failed},
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error deleting jobs: {str(e)}"}
