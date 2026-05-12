"""Batch list all projects in Cloudera AI."""

from typing import Any, Dict
from cmlapi.rest import ApiException
from .http_helpers import setup_client, serialize_result

def batch_list_projects(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """List all projects with pagination."""
    params = params or {}
    try:
        client = setup_client(config["host"], config["api_key"])
        all_projects = []
        page_token = None
        while True:
            kwargs = {"page_size": 100}
            if page_token:
                kwargs["page_token"] = page_token
            result = client.list_projects(**kwargs)
            data = result.to_dict() if hasattr(result, "to_dict") else result
            projects = data.get("projects", [])
            all_projects.extend(projects)
            page_token = data.get("next_page_token")
            if not page_token:
                break
        return {"success": True, "message": f"Found {len(all_projects)} projects", "data": {"projects": all_projects, "count": len(all_projects)}}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
