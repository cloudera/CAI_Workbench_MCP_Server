"""
Create a run for an existing job in Cloudera AI
"""
import os
import json
import requests
from urllib.parse import urlparse
from typing import Dict, Any

def create_job_run(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a run for an existing job in Cloudera AI
    
    Args:
        config: MCP configuration with host and api_key
        params: Parameters for the API call:
            - project_id: ID of the project (required)
            - job_id: ID of the job to run (required)
            - runtime_identifier: Runtime identifier (optional)
            - environment_variables: Dictionary of environment variables (optional)
            - override_config: Dictionary with configuration overrides (optional)
    
    Returns:
        Dict with success flag, message, and job run data
    """
    # Debug prints
    print(f"config type: {type(config)}")
    print(f"config contents: {config}")
    print(f"params type: {type(params)}")
    print(f"params contents: {params}")
    
    # Validate required parameters
    required_params = ["project_id", "job_id"]
    missing_params = [p for p in required_params if p not in params or not params[p]]
    if missing_params:
        return {"success": False, "message": f"Missing required parameters: {', '.join(missing_params)}"}
    
    # Format host URL correctly
    host = config.get("host", "")
    if not host:
        return {"success": False, "message": "Missing host in configuration"}
    
    # Make sure host has the correct scheme
    parsed_url = urlparse(host)
    if not parsed_url.scheme:
        host = "https://" + host
    elif parsed_url.scheme and "://" in host[len(parsed_url.scheme)+3:]:
        # Fix potential double https:// in the URL
        host = parsed_url.scheme + "://" + host.split("://")[-1]
    
    # Remove trailing slash if present
    if host.endswith('/'):
        host = host[:-1]
    
    api_key = config.get("api_key")
    if not api_key:
        return {"success": False, "message": "Missing api_key in configuration"}
    
    # Build the request data
    request_data = {}
    
    # Add optional parameters if provided
    optional_params = {
        "runtime_identifier": "runtime_identifier",
        "environment_variables": "environment_variables",
        "override_config": "override_config"
    }
    
    for param_key, request_key in optional_params.items():
        if param_key in params and params[param_key] is not None:
            request_data[request_key] = params[param_key]
    
    # Debug print URLs
    project_id = params["project_id"]
    job_id = params["job_id"]
    api_url = f"{host}/api/v2/projects/{project_id}/jobs/{job_id}/runs"
    print(f"Creating job run with URL: {api_url}")
    
    # Setup headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Make POST request
        response = requests.post(api_url, headers=headers, json=request_data, timeout=30)
        
        # Check if request was successful
        if response.status_code >= 400:
            try:
                error_data = response.json()
                return {
                    "success": False,
                    "message": f"API error: {error_data.get('error', {}).get('message', 'Unknown error')}",
                    "details": error_data.get("error", {})
                }
            except:
                return {
                    "success": False,
                    "message": f"Failed to create job run: HTTP {response.status_code}"
                }
        
        # Parse the response
        try:
            response_data = response.json()
            
            # Check if there's an error in the response
            if "error" in response_data:
                return {
                    "success": False,
                    "message": f"API error: {response_data.get('error', {}).get('message', 'Unknown error')}",
                    "details": response_data.get("error", {})
                }
            
            return {
                "success": True,
                "message": f"Successfully created run for job '{job_id}'",
                "data": response_data
            }
        except json.JSONDecodeError:
            return {
                "success": False,
                "message": f"Failed to parse response: {response.text}"
            }
    
    except requests.RequestException as e:
        return {
            "success": False,
            "message": f"Error creating job run: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error creating job run: {str(e)}"
        } 