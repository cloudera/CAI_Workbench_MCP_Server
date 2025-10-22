"""Delete job function for Cloudera ML MCP"""

import os
import json
import requests
from urllib.parse import urlparse
from typing import Dict, Any


def delete_job(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delete a job by ID
    
    Args:
        config: MCP configuration with host and api_key
        params: Function parameters
            - job_id: ID of the job to delete
        
    Returns:
        Delete operation results
    """
    # Validate required parameters
    job_id = params.get("job_id")
    if not job_id:
        return {"success": False, "message": "Missing required parameter: job_id"}
    
    # Get project_id from config
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
    
    # Remove trailing slash if present
    host = host.rstrip('/')
    
    api_key = config.get("api_key")
    if not api_key:
        return {"success": False, "message": "Missing api_key in configuration"}
    
    # Setup headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # First, try to get the job details to include in the response
    job_url = f"{host}/api/v2/projects/{project_id}/jobs/{job_id}"
    print(f"Getting job details from: {job_url}")
    
    job_name = f"Job ID {job_id}"
    try:
        # Make GET request to get job details
        job_response = requests.get(job_url, headers=headers, timeout=30)
        
        # If successful, parse the job name
        if job_response.status_code < 400 and job_response.text.strip():
            try:
                job_info = job_response.json()
                job_name = job_info.get("name", job_name)
            except json.JSONDecodeError:
                # If we can't parse the response, continue with deletion anyway
                pass
    except Exception:
        # If we can't get the job details, continue with deletion anyway
        pass
    
    # Build the URL for the delete request
    delete_url = f"{host}/api/v2/projects/{project_id}/jobs/{job_id}"
    print(f"Deleting job with URL: {delete_url}")
    
    try:
        # Make DELETE request
        response = requests.delete(delete_url, headers=headers, timeout=30)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: '{response.text}'")
        
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
                    "message": f"Failed to delete job: HTTP {response.status_code}"
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
                    "message": f"Successfully deleted '{job_name}'",
                    "job_id": job_id,
                    "data": response_data
                }
            except json.JSONDecodeError:
                pass
        
        # If we got here, the deletion was likely successful but returned no content
        return {
            "success": True,
            "message": f"Successfully deleted '{job_name}'",
            "job_id": job_id
        }
    
    except requests.RequestException as e:
        return {
            "success": False,
            "message": f"Error deleting job: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error deleting job: {str(e)}"
        } 