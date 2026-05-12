"""List registered models in Cloudera AI."""

from typing import Any, Dict
from cmlapi.rest import ApiException
from .http_helpers import setup_client, serialize_result

def list_registered_models(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """List registered models."""
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
        result = client.list_registered_models(**kwargs)
        return {"success": True, "message": "list_registered_models ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
