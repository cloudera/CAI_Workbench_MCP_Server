"""Restart a running application in a Cloudera AI project."""

from typing import Any, Dict

from cmlapi.rest import ApiException

from .http_helpers import setup_client, serialize_result


def restart_application(config: Dict[str, str], params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Restart a running application in a Cloudera AI project.

    Args:
        config: MCP configuration with host and api_key
        params: Parameters for the API call:
            - project_id: ID of the project (required, falls back to config)
            - application_id: ID of the application to restart (required)

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

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.restart_application(project_id, application_id)
        return {
            "success": True,
            "message": f"Successfully restarted application {application_id}",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}", "data": None}
    except Exception as e:
        return {"success": False, "message": f"Error restarting application: {str(e)}", "data": None}
