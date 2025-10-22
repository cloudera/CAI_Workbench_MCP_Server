"""Delete project file function for Cloudera ML MCP"""

import os
import json
import requests
from urllib.parse import urlparse, quote
from typing import Dict, Any


def delete_project_file(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delete a file or directory from a Cloudera ML project
    
    Args:
        config: MCP configuration with host and api_key
        params: Function parameters
            - file_path: Path of the file or directory to delete (relative to project root)
            - project_id: ID of the project (optional if in config)
        
    Returns:
        Delete operation results
    """
    # Validate required parameters
    file_path = params.get("file_path")
    if not file_path:
        return {"success": False, "message": "Missing required parameter: file_path"}
    
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
    
    # URL encode the file path
    encoded_file_path = quote(file_path)
    
    # Build the URL for the delete request
    delete_url = f"{host}/api/v2/projects/{project_id}/files?path={encoded_file_path}"
    print(f"Deleting project file with URL: {delete_url}")
    
    # Setup headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
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
                    "message": f"Failed to delete file: HTTP {response.status_code}"
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
                    "message": f"Successfully deleted '{file_path}'",
                    "file_path": file_path,
                    "data": response_data
                }
            except json.JSONDecodeError:
                pass
        
        # If we got here, the deletion was likely successful but returned no content
        return {
            "success": True,
            "message": f"Successfully deleted '{file_path}'",
            "file_path": file_path
        }
    
    except requests.RequestException as e:
        return {
            "success": False,
            "message": f"Error deleting file: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error deleting file: {str(e)}"
        } 