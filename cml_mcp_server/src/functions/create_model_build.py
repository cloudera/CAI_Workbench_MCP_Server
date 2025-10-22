"""
Create a new model build in Cloudera ML
"""
import os
import json
import requests
from urllib.parse import urlparse
from typing import Dict, Any

def create_model_build(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new model build in Cloudera ML
    
    Args:
        config: MCP configuration with host and api_key
        params: Parameters for the API call:
            - project_id: ID of the project (required)
            - model_id: ID of the model to build (required)
            - file_path: Path to the model script file or main Python file (required)
            - function_name: Name of the function that contains the model code (required)
            - kernel: Kernel type (optional, default: python3)
            - runtime_identifier: Runtime identifier (optional)
            - replica_size: Pod size for the build (optional)
            - cpu: CPU cores (optional, default: 1)
            - memory: Memory in GB (optional, default: 2)
            - nvidia_gpu: Number of GPUs (optional, default: 0)
            - use_custom_docker_image: Whether to use a custom Docker image (optional, default: false)
            - custom_docker_image: Custom Docker image to use (optional)
            - environment_variables: Dictionary of environment variables (optional)
    
    Returns:
        Dict with success flag, message, and model build data
    """
    # Validate required parameters
    required_params = ["project_id", "model_id", "file_path", "function_name"]
    missing_params = [p for p in required_params if p not in params or not params[p]]
    if missing_params:
        return {"success": False, "message": f"Missing required parameters: {', '.join(missing_params)}"}
    
    # Check file existence if a local file is provided
    file_path = params["file_path"]
    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                file_content = f.read()
                params["file_path"] = file_content  # Replace path with content
        except Exception as e:
            return {"success": False, "message": f"Failed to read file {file_path}: {str(e)}"}
    
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
        "function_name": params["function_name"],
        "file_path": params["file_path"]
    }
    
    # Add optional parameters if provided
    optional_params = {
        "kernel": "kernel",
        "runtime_identifier": "runtime_identifier",
        "replica_size": "replica_size",
        "cpu": "cpu",
        "memory": "memory",
        "nvidia_gpu": "nvidia_gpu",
        "use_custom_docker_image": "use_custom_docker_image",
        "custom_docker_image": "custom_docker_image",
        "environment_variables": "environment_variables"
    }
    
    for param_key, request_key in optional_params.items():
        if param_key in params and params[param_key] is not None:
            request_data[request_key] = params[param_key]
    
    # Debug print URLs
    project_id = params["project_id"]
    model_id = params["model_id"]
    api_url = f"{host}/api/v2/projects/{project_id}/models/{model_id}/builds"
    print(f"Creating model build with URL: {api_url}")
    
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
                    "message": f"Failed to create model build: HTTP {response.status_code}"
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
                "message": f"Successfully created build for model '{model_id}'",
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
            "message": f"Error creating model build: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error creating model build: {str(e)}"
        } 