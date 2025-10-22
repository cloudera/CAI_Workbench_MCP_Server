"""
Create a new experiment run in Cloudera ML
"""
import os
import json
import requests
from urllib.parse import urlparse
from typing import Dict, Any, List, Optional

def create_experiment_run(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new experiment run in Cloudera ML
    
    Args:
        config: MCP configuration with host and api_key
        params: Parameters for the API call:
            - project_id: Project ID where the experiment run will be created (required)
            - experiment_id: Experiment ID for the run (required)
            - name: Name of the experiment run (optional)
            - description: Description of the experiment run (optional)
            - metrics: Metrics to include in the experiment run (optional, dict)
            - parameters: Parameters for the experiment run (optional, dict)
            - tags: Tags for the experiment run (optional, list of strings)
    
    Returns:
        Dict with success flag, message, and experiment run data
    """
    # Validate required parameters
    required_params = ["project_id", "experiment_id"]
    for param in required_params:
        if param not in params or not params[param]:
            return {"success": False, "message": f"Missing required parameter: {param}"}
    
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
    
    api_key = config.get("api_key")
    if not api_key:
        return {"success": False, "message": "Missing api_key in configuration"}
    
    # Build the request data
    request_data = {}
    
    # Add optional parameters if provided
    if "name" in params and params["name"]:
        request_data["name"] = params["name"]
    
    if "description" in params and params["description"]:
        request_data["description"] = params["description"]
        
    if "metrics" in params and params["metrics"]:
        request_data["metrics"] = params["metrics"]
    
    if "parameters" in params and params["parameters"]:
        request_data["parameters"] = params["parameters"]
    
    if "tags" in params and params["tags"]:
        request_data["tags"] = params["tags"]
    
    # Debug print URLs
    api_url = f"{host}/api/v2/projects/{params['project_id']}/experiments/{params['experiment_id']}/runs"
    print(f"Creating experiment run with URL: {api_url}")
    
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
                    "message": f"Failed to create experiment run: HTTP {response.status_code}"
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
                "message": f"Successfully created experiment run",
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
            "message": f"Error creating experiment run: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error creating experiment run: {str(e)}"
        } 