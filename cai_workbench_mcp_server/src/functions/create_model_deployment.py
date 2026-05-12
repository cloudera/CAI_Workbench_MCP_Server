"""Create a model deployment in Cloudera AI."""

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


def create_model_deployment(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new model deployment."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    model_id = params.get("model_id")
    build_id = params.get("build_id")

    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not model_id:
        return {"success": False, "message": "model_id is required"}
    if not build_id:
        return {"success": False, "message": "build_id is required"}
    if not params.get("name"):
        return {"success": False, "message": "name is required"}

    body = {
        "name": params["name"],
        "cpu": params.get("cpu", 1),
        "memory": params.get("memory", 2),
        "nvidia_gpu": params.get("nvidia_gpu", 0),
        "replica_count": params.get("replica_count", 1),
    }
    if params.get("min_replica_count") is not None:
        body["min_replica_count"] = params["min_replica_count"]
    if params.get("max_replica_count") is not None:
        body["max_replica_count"] = params["max_replica_count"]
    if params.get("enable_auth") is not None:
        body["enable_auth"] = params["enable_auth"]
    if params.get("target_node_selector"):
        body["target_node_selector"] = params["target_node_selector"]
    if params.get("environment_variables"):
        env = params["environment_variables"]
        body["environment_variables"] = json.loads(env) if isinstance(env, str) else env

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.create_model_deployment(body, project_id, model_id, build_id)
        return {"success": True, "message": "Successfully created model deployment", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
