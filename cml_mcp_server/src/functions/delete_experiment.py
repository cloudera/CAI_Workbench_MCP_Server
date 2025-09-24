"""
Delete an experiment in Cloudera ML

SECURITY BEST PRACTICES DEMONSTRATION:
- Shows INCORRECT curl subprocess approach (commented out)
- Shows CORRECT requests library approach (active implementation)
"""
import os
import json
import subprocess
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlparse
from typing import Dict, Any

def delete_experiment(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delete an experiment in Cloudera ML
    
    Args:
        config: MCP configuration with host and api_key
        params: Parameters for the API call:
            - project_id: ID of the project (required)
            - experiment_id: ID of the experiment to delete (required)
    
    Returns:
        Dict with success flag and message
    """
    # Validate required parameters
    required_params = ["project_id", "experiment_id"]
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
    
    # Build the URL for the delete request
    project_id = params["project_id"]
    experiment_id = params["experiment_id"]
    api_url = f"{host}/api/v2/projects/{project_id}/experiments/{experiment_id}"
    print(f"Deleting experiment with URL: {api_url}")
    
    # ❌ INCORRECT PRACTICE - SECURITY VULNERABILITY (commented out)
    # This approach exposes API keys in process list via subprocess arguments
    """
    # Construct curl command - EXPOSES API KEY IN PROCESS LIST!
    curl_cmd = [
        "curl", "-s", "-X", "DELETE",
        "-H", f"Authorization: Bearer {api_key}",  # ⚠️ VISIBLE TO ALL USERS!
        api_url
    ]
    
    # Execute curl command - INSECURE!
    result = subprocess.run(curl_cmd, capture_output=True, text=True)
    """
    
    # ✅ CORRECT PRACTICE - SECURE IMPLEMENTATION
    try:
        # Setup secure session with retries
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Setup secure headers - API key is NOT visible in process list
        headers = {
            "Authorization": f"Bearer {api_key}",  # ✅ SECURE - not in process list
            "Content-Type": "application/json"
        }
        
        # Make secure HTTP request
        response = session.delete(
            api_url,
            headers=headers,
            timeout=30,  # ✅ Explicit timeout
            verify=True  # ✅ SSL verification enabled
        )
        
        # Check response status
        response.raise_for_status()
        
        # Parse the response if there is any content
        if response.text.strip():
            try:
                response_data = response.json()
                
                # Check for API errors
                if "error" in response_data:
                    return {
                        "success": False,
                        "message": f"API error: {response_data.get('error', {}).get('message', 'Unknown error')}"
                        # ✅ Don't expose full error details
                    }
                
                return {
                    "success": True,
                    "message": f"Successfully deleted experiment '{experiment_id}'",
                    "data": response_data
                }
            except ValueError:  # JSON decode error
                # If the response is not JSON, it might be empty for a successful deletion
                pass
        
        # If we got here, the deletion was likely successful but returned no content
        return {
            "success": True,
            "message": f"Successfully deleted experiment '{experiment_id}'"
        }
        
    except requests.exceptions.Timeout:
        return {"success": False, "message": "Request timeout"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "Connection error"}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "message": f"HTTP error: {e.response.status_code}"}
    except requests.exceptions.RequestException:
        return {"success": False, "message": "Request failed"}
    except Exception:
        return {"success": False, "message": "An error occurred"}
        # ✅ Don't expose internal error details 