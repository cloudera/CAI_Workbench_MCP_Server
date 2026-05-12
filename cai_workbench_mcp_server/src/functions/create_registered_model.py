"""Create a registered model in Cloudera AI."""

import json
from typing import Any, Dict

import cmlapi
from cmlapi.rest import ApiException

from .http_helpers import setup_client, serialize_result


def create_registered_model(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Create a registered model."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")

    if not project_id:
        return {"success": False, "message": "project_id is required"}
    for req in ("experiment_id", "run_id", "model_path", "model_name"):
        if not params.get(req):
            return {"success": False, "message": f"{req} is required"}

    # Build the proper request object
    body = cmlapi.CreateRegisteredModelRequest(
        project_id=project_id,
        experiment_id=params["experiment_id"],
        run_id=params["run_id"],
        model_path=params["model_path"],
        model_name=params["model_name"],
    )
    if params.get("description"):
        body.description = params["description"]
    if params.get("notes"):
        body.notes = params["notes"]
    if params.get("visibility"):
        body.visibility = params["visibility"]
    if params.get("tags"):
        tags = params["tags"]
        if isinstance(tags, str):
            try:
                tags = json.loads(tags)
            except json.JSONDecodeError:
                return {"success": False, "message": "tags must be a JSON array string, e.g. '[{\"key\":\"k\",\"value\":\"v\"}]'"}
        # Convert dicts to cmlapi.Tag objects
        body.tags = [cmlapi.Tag(key=t["key"], value=t["value"]) for t in tags]

    try:
        client = setup_client(config["host"], config["api_key"])
        result = client.create_registered_model(body)
        return {"success": True, "message": "Successfully created registered model", "data": serialize_result(result)}
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
