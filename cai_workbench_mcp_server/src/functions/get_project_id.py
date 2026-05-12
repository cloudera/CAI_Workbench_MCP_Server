"""Get project ID by name in Cloudera AI."""

import json
from typing import Any, Dict
try:
    from cmlapi.rest import ApiException
except ImportError:
    ApiException = Exception
from .http_helpers import setup_client, serialize_result

def get_project_id(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Get project ID from a project name."""
    params = params or {}
    project_name = params.get("project_name")
    if not project_name:
        return {"success": False, "message": "project_name is required"}

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

        if project_name == "*":
            formatted = [{"name": p.get("name"), "id": p.get("id"), "owner": p.get("owner")} for p in all_projects]
            return {"status": "success", "projects": formatted, "count": len(formatted)}

        matches = [p for p in all_projects if p.get("name") == project_name]
        if matches:
            p = matches[0]
            return {"status": "success", "project_name": p.get("name"), "project_id": p.get("id"), "owner": p.get("owner")}
        return {"status": "not_found", "message": f"No project found with name '{project_name}'"}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
