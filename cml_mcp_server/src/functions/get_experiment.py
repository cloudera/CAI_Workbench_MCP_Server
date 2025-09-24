"""Get experiment function for Cloudera ML MCP

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


def get_experiment(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get details of a specific experiment from a Cloudera ML project
    
    Args:
        config: MCP configuration with host and api_key
        params: Function parameters
            - experiment_id: ID of the experiment to get details for
            - project_id: ID of the project (optional if in config)
        
    Returns:
        Experiment details
    """
    # Validate required parameters
    if not params.get("experiment_id"):
        return {"success": False, "message": "experiment_id is required"}
    
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
    url = f"{host}/api/v2/projects/{params['project_id']}/experiments/{params['experiment_id']}"
    
    print(f"DEBUG: Accessing URL: {url}")
    
    # ❌ INCORRECT PRACTICE - SECURITY VULNERABILITY (commented out)
    # This approach exposes API keys in process list via subprocess arguments
    """
    # Set up headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.get('api_key', '')}"
    }
    
    # Construct curl command - EXPOSES API KEY IN PROCESS LIST!
    curl_command = [
        "curl", "-s", "-X", "GET",
        "-H", f"Content-Type: {headers['Content-Type']}",
        "-H", f"Authorization: {headers['Authorization']}",  # ⚠️ VISIBLE TO ALL USERS!
        url
    ]
    
    # Execute curl command - INSECURE!
    result = subprocess.run(curl_command, capture_output=True, text=True)
    """
    
    # ✅ CORRECT PRACTICE - SECURE IMPLEMENTATION
    try:
        # Get API key securely
        api_key = config.get('api_key', '')
        if not api_key:
            return {"success": False, "message": "Missing api_key in configuration"}
        
        # Setup secure session with retries
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
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
        response = session.get(
            url,
            headers=headers,
            timeout=30,  # ✅ Explicit timeout
            verify=True  # ✅ SSL verification enabled
        )
        
        # Check response status
        response.raise_for_status()
        
        # Parse response
        response_data = response.json()
        
        return {
            "success": True,
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