"""Create an application in a Cloudera AI project."""

import re
from typing import Any, Dict

from cmlapi.rest import ApiException

from .http_helpers import setup_client, serialize_result


def create_application(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new application in a Cloudera AI project.

    Args:
        config: MCP configuration with host and api_key
        params: Parameters for the API call:
            - project_id: ID of the project (required)
            - name: Name of the application (required)
            - script: Script to run (required)
            - description: Description (optional)
            - subdomain: Subdomain (optional, auto-generated from name if omitted)
            - cpu: CPU cores (optional, default 1)
            - memory: Memory in GB (optional, default 1)
            - nvidia_gpu: Number of GPUs (optional, default 0)
            - runtime_identifier: Runtime identifier (optional)
            - environment_variables: Env vars dict (optional)

    Returns:
        Dict with success flag, message, and data
    """
    required_params = ["project_id", "name", "script"]
    missing = [p for p in required_params if not params.get(p)]
    if missing:
        return {"success": False, "message": f"Missing required parameters: {', '.join(missing)}"}

    project_id = params["project_id"]

    # Build the create body
    body = {
        "name": params["name"],
        "script": params["script"],
        "cpu": params.get("cpu", 1),
        "memory": params.get("memory", 1),
        "nvidia_gpu": params.get("nvidia_gpu", 0),
    }

    # Subdomain: use provided or auto-generate from name
    if params.get("subdomain"):
        body["subdomain"] = params["subdomain"]
    else:
        subdomain = re.sub(r"[^a-z0-9-]", "", params["name"].lower().replace(" ", "-"))
        subdomain = re.sub(r"-+", "-", subdomain).strip("-")
        if subdomain:
            body["subdomain"] = subdomain

    for key in ("description", "runtime_identifier", "environment_variables"):
        if params.get(key):
            body[key] = params[key]

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.create_application(body, project_id)
        return {
            "success": True,
            "message": f"Successfully created application '{params['name']}'",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error creating application: {str(e)}"}
