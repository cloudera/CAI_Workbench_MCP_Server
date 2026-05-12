"""Get available runtimes from Cloudera AI."""

from typing import Any, Dict

try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None

from .http_helpers import setup_client


def get_runtimes(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get available runtimes from Cloudera AI.

    Args:
        config: MCP configuration with host and api_key
        params: Function parameters (optional query filters):
            - search_filter: Filter string (optional)
            - page_size: Number of results per page (optional)
            - page_token: Pagination token (optional)

    Returns:
        Dict with success flag, message, and runtimes list
    """
    try:
        client = setup_client(config["host"], config["api_key"])

        kwargs = {}
        if params.get("search_filter"):
            kwargs["search_filter"] = params["search_filter"]
        if params.get("page_size"):
            kwargs["page_size"] = params["page_size"]
        if params.get("page_token"):
            kwargs["page_token"] = params["page_token"]

        result = client.list_runtimes(**kwargs)
        runtimes_list = result.to_dict() if hasattr(result, "to_dict") else result

        runtimes = runtimes_list.get("runtimes", [])
        formatted = []
        for rt in runtimes:
            formatted.append({
                "identifier": rt.get("image_identifier", ""),
                "edition": rt.get("edition", "Unknown"),
                "editor": rt.get("editor", "Unknown"),
                "kernel": rt.get("kernel", "Unknown"),
                "full_version": rt.get("full_version", ""),
            })

        return {
            "success": True,
            "message": f"Found {len(formatted)} available runtimes",
            "runtimes": formatted,
            "count": len(formatted),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error retrieving runtimes: {str(e)}"}
