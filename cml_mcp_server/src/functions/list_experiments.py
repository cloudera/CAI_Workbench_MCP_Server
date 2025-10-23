"""Function to list experiments in a Cloudera AI project."""

import json
import os
import requests
from urllib.parse import urlparse


def list_experiments(config, params=None):
    """
    List experiments in a Cloudera AI project.

    Args:
        config (dict): MCP configuration.
        params (dict, optional): Parameters for the API call. Default is None.
            - project_id (str, optional): ID of the project to list experiments from.
                If not provided, it will be taken from the configuration.

    Returns:
        dict: Response with the following structure:
            {
                "success": bool,
                "message": str,
                "data": list  # List of experiment objects if successful, otherwise None
            }
    """
    params = params or {}
    project_id = params.get('project_id') or config.get('project_id')

    if not project_id:
        return {
            "success": False,
            "message": "project_id is required either in config or params",
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
    url = f"{host}/api/v2/projects/{project_id}/experiments"
    
    print(f"Accessing: {url}")

    # Setup headers
    headers = {
        "Authorization": f"Bearer {config.get('api_key', '')}",
        "Content-Type": "application/json"
    }

    # Execute the request
    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code >= 400:
            return {
                "success": False,
                "message": f"Failed to execute request: HTTP {response.status_code}",
                "data": None
            }

        try:
            data = response.json()
            return {
                "success": True,
                "message": "Successfully listed experiments",
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
    except Exception as e:
        return {
            "success": False,
            "message": f"An unexpected error occurred: {str(e)}",
            "data": None
        } 