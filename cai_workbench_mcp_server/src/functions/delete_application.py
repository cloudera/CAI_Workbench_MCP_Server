"""Delete an application in Cloudera AI."""

from typing import Any, Dict

from cmlapi.rest import ApiException

from .http_helpers import setup_client, serialize_result


def delete_application(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delete an application in Cloudera AI.

    Args:
        config: MCP configuration with host and api_key
        params: Parameters for the API call:
            - project_id: ID of the project (required)
            - application_id: ID of the application to delete (required)

    Returns:
        Dict with success flag and message
    """
    project_id = params.get("project_id")
    application_id = params.get("application_id")

    if not project_id or not application_id:
        missing = [p for p in ("project_id", "application_id") if not params.get(p)]
        return {"success": False, "message": f"Missing required parameters: {', '.join(missing)}"}

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.delete_application(project_id, application_id)
        return {
            "success": True,
            "message": f"Successfully deleted application '{application_id}'",
            "data": serialize_result(result),
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error deleting application: {str(e)}"}
