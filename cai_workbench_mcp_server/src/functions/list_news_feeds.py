"""List news feeds in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

def list_news_feeds(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """List news feeds for a category."""
    params = params or {}
    category = params.get("category")
    if not category:
        return {"success": False, "message": "category is required"}
    kwargs = {}
    if params.get("page_size"):
        kwargs["page_size"] = params["page_size"]
    if params.get("page_token"):
        kwargs["page_token"] = params["page_token"]
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.list_news_feeds(category, **kwargs)
        return {"success": True, "message": "list_news_feeds ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
