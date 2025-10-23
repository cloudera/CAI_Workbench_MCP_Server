"""
Create a new experiment in Cloudera AI

SECURITY BEST PRACTICES DEMONSTRATION:
- Shows INCORRECT curl subprocess approach (commented out)
- Shows CORRECT requests library approach (active implementation)
"""
import os
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlparse
from typing import Dict, Any, List, Optional

def create_experiment(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new experiment in Cloudera AI
    
    Args:
        config: MCP configuration with host and api_key
        params: Parameters for the API call:
            - project_id: Project ID where the experiment will be created (required)
            - name: Name of the experiment (required)
            - description: Description of the experiment (optional)
    
    Returns:
        Dict with success flag, message, and experiment data
    """
    # Validate required parameters
    required_params = ["project_id", "name"]
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
    request_data = {
        "name": params["name"]
    }
    
    # Add description if provided
    if "description" in params and params["description"]:
        request_data["description"] = params["description"]
    
    # Debug print URLs
    api_url = f"{host}/api/v2/projects/{params['project_id']}/experiments"
    print(f"Creating experiment with URL: {api_url}")
    
    # ❌ INCORRECT PRACTICE - SECURITY VULNERABILITY (commented out)
    # This approach exposes API keys in process list via subprocess arguments
    
    # ✅ CORRECT PRACTICE - SECURE IMPLEMENTATION
    try:
        # Setup secure session with retries
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS", "POST"]
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
        response = session.post(
            api_url,
            json=request_data,
            headers=headers,
            timeout=30,  # ✅ Explicit timeout
            verify=True  # ✅ SSL verification enabled
        )
        
        # Check response status
        response.raise_for_status()
        
        # Parse response
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
            "message": "Successfully created experiment",
            "data": response_data
        }
        
    except requests.exceptions.Timeout:
        return {"success": False, "message": "Request timeout"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "Connection error"}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "message": f"HTTP error: {e.response.status_code}"}
    except requests.exceptions.RequestException:
        return {"success": False, "message": "Request failed"}
    except ValueError:  # JSON decode error
        return {"success": False, "message": "Invalid response format"}
    except Exception:
        return {"success": False, "message": "An error occurred"}
        # ✅ Don't expose internal error details 