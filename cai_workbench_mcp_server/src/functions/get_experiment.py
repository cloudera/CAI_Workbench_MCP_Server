"""Get experiment in Cloudera AI."""

from typing import Any, Dict

try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None

from .http_helpers import setup_client, serialize_result


def get_experiment(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Get experiment in Cloudera AI."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    experiment_id = params.get("experiment_id")
    if not experiment_id:
        return {"success": False, "message": "experiment_id is required"}

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.get_experiment(project_id, experiment_id)
        return {
            "success": True,
            "message": f"Successfully getd experiment",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
