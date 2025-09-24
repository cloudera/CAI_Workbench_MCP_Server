"""Function to update an experiment in a Cloudera ML project.

SECURITY BEST PRACTICES DEMONSTRATION:
- Shows INCORRECT curl subprocess approach (commented out)
- Shows CORRECT requests library approach (active implementation)
"""

import json
import os
import subprocess
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlparse


def update_experiment(config, params=None):
    """
    Update an experiment in a Cloudera ML project.

    Args:
        config (dict): MCP configuration.
        params (dict, optional): Parameters for the API call. Default is None.
            - project_id (str, optional): ID of the project.
                If not provided, it will be taken from the configuration.
            - experiment_id (str): ID of the experiment to update.
            - name (str, optional): New name for the experiment.
            - description (str, optional): New description for the experiment.

    Returns:
        dict: Response with the following structure:
            {
                "success": bool,
                "message": str,
                "data": dict  # Result data if successful, otherwise None
            }
    """
    params = params or {}
    project_id = params.get('project_id') or config.get('project_id')
    experiment_id = params.get('experiment_id')

    if not project_id:
        return {
            "success": False,
            "message": "project_id is required either in config or params",
            "data": None
        }

    if not experiment_id:
        return {
            "success": False,
            "message": "experiment_id is required in params",
            "data": None
        }

    # Format host URL
    host = config.get('host', '')
    if not host:
        return {
            "success": False,
            "message": "host is required in config",
            "data": None
        }

    # Ensure the host has the correct scheme and no trailing slash
    parsed_url = urlparse(host)
    if not parsed_url.scheme:
        host = 'https://' + host
    elif host.startswith('http://'):
        host = 'https://' + host[7:]

    host = host.rstrip('/')

    # Build the API URL
    url = f"{host}/api/v2/projects/{project_id}/experiments/{experiment_id}"
    
    print(f"Accessing: {url}")

    # Prepare request data
    request_data = {}
    
    # Add optional parameters to request data
    for key in ['name', 'description']:
        if params.get(key) is not None:
            request_data[key] = params[key]
    
    # ❌ INCORRECT PRACTICE - SECURITY VULNERABILITY (commented out)
    # This approach exposes API keys in process list via subprocess arguments
    """
    # Prepare the curl command - EXPOSES API KEY IN PROCESS LIST!
    curl_command = [
        'curl', '-s',
        '-X', 'PATCH',
        '-H', f"Authorization: Bearer {config.get('api_key', '')}",  # ⚠️ VISIBLE TO ALL USERS!
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(request_data),
        url
    ]

    # Execute curl command - INSECURE!
    response = subprocess.run(curl_command, capture_output=True, text=True, check=False)
    """
    
    # ✅ CORRECT PRACTICE - SECURE IMPLEMENTATION
    try:
        # Get API key securely
        api_key = config.get('api_key', '')
        if not api_key:
            return {"success": False, "message": "Missing api_key in configuration", "data": None}
        
        # Setup secure session with retries
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS", "PATCH"]
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
        response = session.patch(
            url,
            json=request_data,
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
            "message": f"Successfully updated experiment {experiment_id}",
            "data": response_data
        }
        
    except requests.exceptions.Timeout:
        return {"success": False, "message": "Request timeout", "data": None}
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "Connection error", "data": None}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "message": f"HTTP error: {e.response.status_code}", "data": None}
    except requests.exceptions.RequestException:
        return {"success": False, "message": "Request failed", "data": None}
    except ValueError:  # JSON decode error
        return {"success": False, "message": "Invalid response format", "data": None}
    except Exception:
        return {"success": False, "message": "An error occurred", "data": None}
        # ✅ Don't expose internal error details 