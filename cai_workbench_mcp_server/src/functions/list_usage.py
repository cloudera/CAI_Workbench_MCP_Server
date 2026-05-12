"""Cloudera AI: list_usage."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

def list_usage(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """list_usage."""
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
    if params.get("multi_column_search_filter"):
        kwargs["multi_column_search_filter"] = params["multi_column_search_filter"]
    if params.get("time_range_search_filter"):
        kwargs["time_range_search_filter"] = params["time_range_search_filter"]
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.list_usage(**kwargs)
        return {"success": True, "message": "list_usage ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
