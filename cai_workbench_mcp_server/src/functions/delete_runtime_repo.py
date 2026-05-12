"""Delete a runtime repo in Cloudera AI."""

from typing import Any, Dict
from cmlapi.rest import ApiException
from .http_helpers import setup_client, serialize_result

def delete_runtime_repo(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Delete a runtime repo."""
    params = params or {}
    runtime_repo_id = params.get("runtime_repo_id")
    if not runtime_repo_id:
        return {"success": False, "message": "runtime_repo_id is required"}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.delete_runtime_repo(int(runtime_repo_id))
        return {"success": True, "message": f"Successfully deleted runtime repo '{runtime_repo_id}'", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
