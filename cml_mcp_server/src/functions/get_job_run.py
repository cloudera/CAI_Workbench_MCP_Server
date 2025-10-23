"""Get job run function for Cloudera AI Workbench MCP"""

import os
import json
import requests
from urllib.parse import urlparse
from typing import Dict, Any


def get_job_run(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get details of a specific job run from a Cloudera AI project
    
    Args:
        config: MCP configuration with host and api_key
        params: Function parameters
            - job_id: ID of the job containing the run
            - run_id: ID of the job run to get details for
            - project_id: ID of the project (optional if in config)
        
    Returns:
        Job run details
    """
    # Validate required parameters
    if not params.get("job_id"):
        return {"success": False, "message": "job_id is required"}
    
    if not params.get("run_id"):
        return {"success": False, "message": "run_id is required"}
    
    if not params.get("project_id"):
        if not config.get("project_id"):
            return {"success": False, "message": "project_id is required either in config or params"}
        params["project_id"] = config.get("project_id")
    
    # Format host URL
    host = config.get("host", "")
    parsed_url = urlparse(host)
    
    # Ensure the host has the correct scheme
    if not parsed_url.scheme:
        host = f"https://{host}"
    elif "https://" in parsed_url.netloc:
        # Handle cases where the host already contains https:// in the netloc
        host = f"{parsed_url.scheme}://{parsed_url.netloc.replace('https://', '')}{parsed_url.path}"
    
    # Construct API URL
    url = f"{host}/api/v2/projects/{params['project_id']}/jobs/{params['job_id']}/runs/{params['run_id']}"
    
    # Set up headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.get('api_key', '')}"
    }
    
    print(f"DEBUG: Accessing URL: {url}")
    
    try:
        # Make GET request
        response = requests.get(url, headers=headers, timeout=30)
        
        # Check if request was successful
        if response.status_code >= 400:
            return {
                "success": False,
                "message": f"API request failed with HTTP {response.status_code}",
                "error": response.text
            }
        
        try:
            response_data = response.json()
            return {
                "success": True,
                "data": response_data
            }
        except json.JSONDecodeError:
            return {
                "success": False,
                "message": "Failed to parse API response",
                "raw_response": response.text
            }
    
    except requests.RequestException as e:
        return {
            "success": False,
            "message": f"Error executing request: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error executing request: {str(e)}"
        } 