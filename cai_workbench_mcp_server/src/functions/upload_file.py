"""Upload a file to a Cloudera AI project."""

import os
import requests
from typing import Any, Dict
from .http_helpers import normalize_host, auth_headers

def upload_file(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """Upload a single file to a project."""
    params = params or {}
    project_id = params.get("project_id") or config.get("project_id")
    file_path = params.get("file_path")
    if not project_id:
        return {"success": False, "message": "project_id is required"}
    if not file_path:
        return {"success": False, "message": "file_path is required"}
    if not os.path.isfile(file_path):
        return {"success": False, "message": f"Error uploading file: {file_path} is not a valid file"}

    target_name = params.get("target_name") or os.path.basename(file_path)
    target_dir = params.get("target_dir") or ""
    target_path = os.path.join(target_dir, target_name) if target_dir else target_name

    host = normalize_host(config["host"])
    url = f"{host}/api/v2/projects/{project_id}/files"
    headers = {"Authorization": f"Bearer {config['api_key']}"}

    try:
        with open(file_path, "rb") as f:
            files_payload = {target_path: f}
            response = requests.put(url, headers=headers, files=files_payload, timeout=60)
        if response.status_code in (200, 201, 202, 204):
            return {"success": True, "message": f"Successfully uploaded file: {target_name}", "file_path": file_path, "target_name": target_name, "target_dir": target_dir, "target_path": target_path}
        return {"success": False, "message": f"Upload failed: HTTP {response.status_code} - {response.text}"}
    except Exception as e:
        return {"success": False, "message": f"Error uploading file: {str(e)}"}
