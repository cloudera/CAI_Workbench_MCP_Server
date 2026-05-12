"""Update a runtime repo in Cloudera AI."""

import json
from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

def update_runtime_repo(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Update runtime repo."""
    params = params or {}
    runtimerepo_id = params.get("runtimerepo_id")
    body_json = params.get("body_json")
    if not runtimerepo_id:
        return {"success": False, "message": "runtimerepo_id is required"}
    if not body_json:
        return {"success": False, "message": "body_json is required"}
    body = json.loads(body_json) if isinstance(body_json, str) else body_json
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.update_runtime_repo(body, int(runtimerepo_id))
        return {"success": True, "message": "update_runtime_repo ok", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
