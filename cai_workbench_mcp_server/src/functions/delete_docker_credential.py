"""Delete a Docker credential in Cloudera AI."""

from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result

def delete_docker_credential(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Delete a Docker credential."""
    params = params or {}
    docker_credential_id = params.get("docker_credential_id")
    if not docker_credential_id:
        return {"success": False, "message": "docker_credential_id is required"}
    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.delete_docker_credential(docker_credential_id)
        return {"success": True, "message": f"Successfully deleted credential '{docker_credential_id}'", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
