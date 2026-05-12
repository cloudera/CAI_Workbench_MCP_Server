"""Cloudera AI: list_docker_credentials."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

def list_docker_credentials(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """list_docker_credentials."""
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
        result = client.list_docker_credentials(**kwargs)
        return {"success": True, "message": "list_docker_credentials ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
