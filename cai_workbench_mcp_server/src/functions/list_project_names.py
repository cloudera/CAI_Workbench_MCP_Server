"""List project names in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception
from .http_helpers import setup_client, serialize_result

def list_project_names(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """List project names."""
    params = params or {}
    kwargs = {}
    for k in ("search_filter", "page_size", "page_token", "sort"):
        if params.get(k):
            kwargs[k] = params[k]
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.list_project_names(**kwargs)
        return {"success": True, "message": "list_project_names ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
