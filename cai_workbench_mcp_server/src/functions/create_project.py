"""Create a project in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

DEFAULT_TEMPLATE = "blank"
DEFAULT_ENGINE_TYPE = "ml_runtime"


def create_project(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new project."""
    params = params or {}
    if not params.get("name"):
        return {"success": False, "message": "name is required"}

    body = {
        "name": params["name"],
        "template": params.get("template") or DEFAULT_TEMPLATE,
        "default_project_engine_type": params.get("default_project_engine_type") or DEFAULT_ENGINE_TYPE,
    }
    if params.get("description"):
        body["description"] = params["description"]

    team_name = params.get("team_name") or config.get("team")
    if team_name:
        body["team_name"] = team_name

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.create_project(body)
        return {"success": True, "message": "Successfully executed create_project", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
