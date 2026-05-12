"""Update an application in a Cloudera AI project."""

from typing import Any, Dict

try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None

from .http_helpers import setup_client, serialize_result


def update_application(config: Dict[str, str], params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Update an application in a Cloudera AI project.

    Args:
        config: MCP configuration with host and api_key
        params: Parameters for the API call:
            - project_id: ID of the project (required, falls back to config)
            - application_id: ID of the application to update (required)
            - name: New name (optional)
            - description: New description (optional)
            - script: New script path (optional)
            - cpu: CPU cores (optional)
            - memory: Memory in GB (optional)
            - nvidia_gpu: GPU count (optional)
            - environment_variables: Env vars dict (optional)
            - runtime_identifier: Runtime identifier (optional)

    Returns:
        Dict with success flag, message, and data
    """
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    application_id = params.get("application_id")

    if not project_id:
        return {"success": False, "message": "project_id is required either in config or params", "data": None}
    if not application_id:
        return {"success": False, "message": "application_id is required in params", "data": None}

    # Build the update body from optional params
    update_fields = {}
    for key in ("name", "description", "script", "cpu", "memory", "nvidia_gpu",
                "environment_variables", "runtime_identifier"):
        if params.get(key) is not None:
            update_fields[key] = params[key]

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.update_application(update_fields, project_id, application_id)
        return {
            "success": True,
            "message": f"Successfully updated application {application_id}",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}", "data": None}
    except Exception as e:
        return {"success": False, "message": f"Error updating application: {str(e)}", "data": None}
