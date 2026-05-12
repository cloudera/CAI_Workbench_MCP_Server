"""Create a model build in Cloudera AI."""

import json
from typing import Any, Dict

from cmlapi.rest import ApiException

from .http_helpers import setup_client, serialize_result


def create_model_build(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new model build."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    model_id = params.get("model_id")

    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not model_id:
        return {"success": False, "message": "model_id is required"}
    if not params.get("file_path"):
        return {"success": False, "message": "file_path is required"}
    if not params.get("function_name"):
        return {"success": False, "message": "function_name is required"}

    body = {
        "file_path": params["file_path"],
        "function_name": params["function_name"],
        "kernel": params.get("kernel", "python3"),
        "cpu": params.get("cpu", 1),
        "memory": params.get("memory", 2),
        "nvidia_gpu": params.get("nvidia_gpu", 0),
    }
    if params.get("runtime_identifier"):
        body["runtime_identifier"] = params["runtime_identifier"]
    if params.get("replica_size"):
        body["replica_size"] = params["replica_size"]
    if params.get("use_custom_docker_image"):
        body["use_custom_docker_image"] = params["use_custom_docker_image"]
    if params.get("custom_docker_image"):
        body["custom_docker_image"] = params["custom_docker_image"]
    if params.get("environment_variables"):
        env = params["environment_variables"]
        body["environment_variables"] = json.loads(env) if isinstance(env, str) else env

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.create_model_build(body, project_id, model_id)
        return {"success": True, "message": "Successfully created model build", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
