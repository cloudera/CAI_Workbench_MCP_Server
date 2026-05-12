"""Create a project in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception
from .http_helpers import setup_client, serialize_result

def create_project(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new project."""
    params = params or {}
    if not params.get("name"):
        return {"success": False, "message": "name is required"}
    body = {"name": params["name"]}
    if params.get("description"):
        body["description"] = params["description"]
    if params.get("template"):
        body["template"] = params["template"]
    if params.get("default_project_engine_type"):
        body["default_project_engine_type"] = params["default_project_engine_type"]
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.create_project(body)
        return {"success": True, "message": f"Successfully executed create_project", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
