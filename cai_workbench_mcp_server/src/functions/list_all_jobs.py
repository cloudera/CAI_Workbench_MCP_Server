"""List all jobs in Cloudera AI."""

from typing import Any, Dict

try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception

from .http_helpers import setup_client, serialize_result


def list_all_jobs(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """List all jobs in Cloudera AI."""
    params = params or {}

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
        result = client.list_all_jobs(**kwargs)
        return {
            "success": True,
            "message": "list_all_jobs ok",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
