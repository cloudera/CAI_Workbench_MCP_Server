"""Bulk log experiment run details (metrics, params, tags) in one request."""

import json
import requests
from urllib.parse import urlparse
from typing import Dict, Any


def log_experiment_run_batch(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Bulk update experiment run details like metrics, params, and tags in one request.

    Args:
        config: MCP configuration with host and api_key
        params: Parameters for the API call:
            - project_id (str): ID of the project (required)
            - experiment_id (str): ID of the experiment (required)
            - run_id (str): ID of the experiment run to log under (required)
            - metrics (list): List of metric objects [{key, value, timestamp, step}] (optional)
            - params_list (list): List of param objects [{key, value}] (optional)
            - tags (list): List of tag objects [{key, value}] (optional)
            - model_json (str): MLmodel file in JSON format (optional)

    Returns:
        Dict with success flag, message, and response data
    """
    # Validate required parameters
    project_id = params.get("project_id") or config.get("project_id")
    experiment_id = params.get("experiment_id")
    run_id = params.get("run_id")

    if not project_id:
        return {"success": False, "message": "project_id is required", "data": None}
    if not experiment_id:
        return {"success": False, "message": "experiment_id is required", "data": None}
    if not run_id:
        return {"success": False, "message": "run_id is required", "data": None}

    # Get batch data
    metrics = params.get("metrics", [])
    params_list = params.get("params_list", [])
    tags = params.get("tags", [])
    model_json = params.get("model_json")

    if not metrics and not params_list and not tags and not model_json:
        return {
            "success": False,
            "message": "At least one of metrics, params_list, tags, or model_json must be provided",
            "data": None
        }

    # Format host URL
    host = config.get("host", "")
    if not host:
        return {"success": False, "message": "Missing host in configuration", "data": None}

    parsed_url = urlparse(host)
    if not parsed_url.scheme:
        host = "https://" + host
    elif host.startswith("http://"):
        host = "https://" + host[7:]

    host = host.rstrip("/")

    api_key = config.get("api_key")
    if not api_key:
        return {"success": False, "message": "Missing api_key in configuration", "data": None}

    # Build the URL per swagger: POST .../runs/{run_id}:logbatch
    url = f"{host}/api/v2/projects/{project_id}/experiments/{experiment_id}/runs/{run_id}:logbatch"

    # Prepare payload matching swagger schema
    payload = {}
    if metrics:
        payload["metrics"] = metrics
    if params_list:
        payload["params"] = params_list
    if tags:
        payload["tags"] = tags
    if model_json:
        payload["model_json"] = model_json

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code >= 400:
            try:
                error_data = response.json()
                return {
                    "success": False,
                    "message": f"API error (HTTP {response.status_code}): {error_data.get('message', response.text)}",
                    "data": error_data
                }
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "message": f"API error: HTTP {response.status_code} - {response.text}",
                    "data": None
                }

        try:
            data = response.json()
        except json.JSONDecodeError:
            data = None

        return {
            "success": True,
            "message": f"Successfully logged batch data to experiment run {run_id}",
            "data": data
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "message": f"Request error: {str(e)}",
            "data": None
        }
