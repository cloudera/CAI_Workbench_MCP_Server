"""Delete model function for Cloudera AI Workbench MCP"""

import os
import json
import requests
from urllib.parse import urlparse
from typing import Dict, Any


def delete_model(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delete a model by ID
    
    Args:
        config: MCP configuration with host and api_key
        params: Function parameters
            - model_id: ID of the model to delete
            - project_id: ID of the project containing the model (optional if in config)
        
    Returns:
        Delete operation results
    """
    # Validate required parameters
    model_id = params.get("model_id")
    if not model_id:
        return {"success": False, "message": "Missing required parameter: model_id"}
    
    # Get project_id from params or config
    project_id = params.get("project_id") or config.get("project_id")
    if not project_id:
        return {"success": False, "message": "Missing project_id in configuration or parameters"}
    
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
    
    # Setup headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # First, try to get the model details to include in the response
    model_url = f"{host}/api/v2/projects/{project_id}/models/{model_id}"
    print(f"Getting model details from: {model_url}")
    
    model_name = f"Model ID {model_id}"
    try:
        # Make GET request to get model details
        model_response = requests.get(model_url, headers=headers, timeout=30)
        
        # If successful, parse the model name
        if model_response.status_code < 400 and model_response.text.strip():
            try:
                model_info = model_response.json()
                model_name = model_info.get("name", model_name)
            except json.JSONDecodeError:
                # If we can't parse the response, continue with deletion anyway
                pass
    except Exception:
        # If we can't get the model details, continue with deletion anyway
        pass
    
    # Build the URL for the delete request
    delete_url = f"{host}/api/v2/projects/{project_id}/models/{model_id}"
    print(f"Deleting model with URL: {delete_url}")
    
    try:
        # Make DELETE request
        response = requests.delete(delete_url, headers=headers, timeout=30)
        
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
                    "message": f"Failed to delete model: HTTP {response.status_code}"
                }
        
        # Parse response if there is content
        if response.text.strip():
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
                    "message": f"Successfully deleted model '{model_name}'",
                    "model_id": model_id,
                    "data": response_data
                }
            except json.JSONDecodeError:
                pass
        
        # If we got here, the deletion was likely successful but returned no content
        return {
            "success": True,
            "message": f"Successfully deleted model '{model_name}'",
            "model_id": model_id
        }
    
    except requests.RequestException as e:
        return {
            "success": False,
            "message": f"Error deleting model: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error deleting model: {str(e)}"
        } 