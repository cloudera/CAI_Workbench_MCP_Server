"""Function to stop a model deployment in a Cloudera AI project."""

import json
import requests
from urllib.parse import urlparse


def stop_model_deployment(config, params=None):
    """
    Stop a model deployment in a Cloudera AI project.

    Args:
        config (dict): MCP configuration.
        params (dict, optional): Parameters for the API call. Default is None.
            - project_id (str, optional): ID of the project.
                If not provided, it will be taken from the configuration.
            - model_id (str): ID of the model containing the deployment.
            - build_id (str): ID of the build containing the deployment.
            - deployment_id (str): ID of the model deployment to stop.

    Returns:
        dict: Response with the following structure:
            {
                "success": bool,
                "message": str,
                "data": dict  # Result data if successful, otherwise None
            }
    """
    params = params or {}
    project_id = params.get('project_id') or config.get('project_id')
    model_id = params.get('model_id')
    build_id = params.get('build_id')
    deployment_id = params.get('deployment_id')

    if not project_id:
        return {
            "success": False,
            "message": "project_id is required either in config or params",
            "data": None
        }

    if not model_id:
        return {
            "success": False,
            "message": "model_id is required in params",
            "data": None
        }

    if not build_id:
        return {
            "success": False,
            "message": "build_id is required in params",
            "data": None
        }

    if not deployment_id:
        return {
            "success": False,
            "message": "deployment_id is required in params",
            "data": None
        }

    # Format host URL
    host = config.get('host', '')
    if not host:
        return {
            "success": False,
            "message": "host is required in config",
            "data": None
        }

    # Ensure the host has the correct scheme and no trailing slash
    parsed_url = urlparse(host)
    if not parsed_url.scheme:
        host = 'https://' + host
    elif host.startswith('http://'):
        host = 'https://' + host[7:]

    host = host.rstrip('/')

    # Build the API URL
    url = f"{host}/api/v2/projects/{project_id}/models/{model_id}/builds/{build_id}/deployments/{deployment_id}:stop"

    # Setup headers
    headers = {
        "Authorization": f"Bearer {config.get('api_key', '')}",
        "Content-Type": "application/json"
    }

    # Execute the request
    try:
        response = requests.post(url, headers=headers, timeout=30)

        if response.status_code >= 400:
            return {
                "success": False,
                "message": f"Failed to stop model deployment: HTTP {response.status_code} - {response.text}",
                "data": None
            }

        try:
            data = response.json()
            return {
                "success": True,
                "message": f"Successfully stopped model deployment {deployment_id}",
                "data": data
            }
        except json.JSONDecodeError:
            return {
                "success": False,
                "message": f"Failed to parse response as JSON: {response.text}",
                "data": None
            }
    except requests.RequestException as e:
        return {
            "success": False,
            "message": f"Failed to execute request: {str(e)}",
            "data": None
        }
