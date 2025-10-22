"""
Create a new model deployment in Cloudera ML
"""
import os
import json
import requests
from urllib.parse import urlparse
from typing import Dict, Any

def create_model_deployment(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new model deployment in Cloudera ML
    
    Args:
        config: MCP configuration with host and api_key
        params: Parameters for the API call:
            - project_id: ID of the project (required)
            - model_id: ID of the model to deploy (required)
            - build_id: ID of the model build to deploy (required)
            - name: Name of the deployment (required)
            - cpu: CPU cores (optional, default: 1)
            - memory: Memory in GB (optional, default: 2)
            - replica_count: Number of replicas (optional, default: 1)
            - min_replica_count: Minimum number of replicas (optional)
            - max_replica_count: Maximum number of replicas (optional)
            - nvidia_gpu: Number of GPUs (optional, default: 0)
            - environment_variables: Dictionary of environment variables (optional)
            - enable_auth: Whether to enable authentication (optional, default: true)
            - target_node_selector: Target node selector for the deployment (optional)
    
    Returns:
        Dict with success flag, message, and model deployment data
    """
    # Validate required parameters
    required_params = ["project_id", "model_id", "build_id", "name"]
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
    
    api_key = config.get("api_key")
    if not api_key:
        return {"success": False, "message": "Missing api_key in configuration"}
    
    # Build the request data
    request_data = {
        "name": params["name"],
        "build_id": params["build_id"]
    }
    
    # Add optional parameters if provided
    optional_params = {
        "cpu": "cpu",
        "memory": "memory",
        "replica_count": "replica_count",
        "min_replica_count": "min_replica_count",
        "max_replica_count": "max_replica_count",
        "nvidia_gpu": "nvidia_gpu",
        "environment_variables": "environment_variables",
        "enable_auth": "enable_auth",
        "target_node_selector": "target_node_selector"
    }
    
    for param_key, request_key in optional_params.items():
        if param_key in params and params[param_key] is not None:
            request_data[request_key] = params[param_key]
    
    # Debug print URLs
    project_id = params["project_id"]
    model_id = params["model_id"]
    api_url = f"{host}/api/v2/projects/{project_id}/models/{model_id}/deployments"
    print(f"Creating model deployment with URL: {api_url}")
    
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
                    "message": f"Failed to create model deployment: HTTP {response.status_code}"
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
                "message": f"Successfully created deployment '{params['name']}' for model '{model_id}'",
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
            "message": f"Error creating model deployment: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error creating model deployment: {str(e)}"
        } 