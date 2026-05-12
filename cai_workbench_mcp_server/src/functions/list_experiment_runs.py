"""List experiment runs in Cloudera AI."""

from typing import Any, Dict

try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception

from .http_helpers import setup_client, serialize_result


def list_experiment_runs(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """List experiment runs in Cloudera AI."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    experiment_id = params.get("experiment_id")
    if not experiment_id:
        return {"success": False, "message": "experiment_id is required"}

    kwargs = {}
    if params.get("search_filter"):
        kwargs["search_filter"] = params["search_filter"]
    if params.get("page_size"):
        kwargs["page_size"] = params["page_size"]
    if params.get("page_token"):
        kwargs["page_token"] = params["page_token"]
    if params.get("sort"):
        kwargs["sort"] = params["sort"]

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.list_experiment_runs(project_id, experiment_id, **kwargs)
        return {
            "success": True,
            "message": "list_experiment_runs ok",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
