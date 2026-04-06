"""Create a new project. function for Cloudera AI Workbench MCP"""

import requests
import json
from typing import Dict, Any

def create_project(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new project.
    
    Args:
        config: MCP configuration with host and api_key
        params: Function parameters
            - name (required)
            - description (optional)
            - template (optional)
            - default_project_engine_type (optional)
        
    Returns:
        create_project results
    """
    try:
        # Validate required parameters
        required_params = ['name']
        missing_params = [p for p in required_params if p not in params or not params[p]]
        if missing_params:
            return {"success": False, "message": f"Missing required parameters: {', '.join(missing_params)}"}
            
        # Format host URL correctly
        host = config.get("host", "").strip()
        if host.startswith("https://https://"):
            host = host.replace("https://https://", "https://")
        if not host.startswith(("http://", "https://")):
            host = "https://" + host
        host = host.rstrip("/")
        
        api_key = config.get("api_key")
        if not api_key:
            return {"success": False, "message": "Missing api_key in configuration"}
            
        # Prepare request payload
        payload = {}
        payload["name"] = params["name"]
        if "description" in params:
            payload["description"] = params["description"]
        if "template" in params:
            payload["template"] = params["template"]
        if "default_project_engine_type" in params:
            payload["default_project_engine_type"] = params["default_project_engine_type"]

        
        # Build the URL for the request
        api_url = f"{host}/api/v2/projects"

        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Make the request
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        # Parse the response
        try:
            data = response.json()
        except:
            data = {"message": "Success", "text": response.text}
        
        return {
            "success": True,
            "message": "Successfully executed create_project",
            "data": data
        }
        
    except requests.exceptions.RequestException as e:
        error_message = str(e)
        response_body = ""
        if hasattr(e, 'response') and e.response is not None:
            try:
                response_body = e.response.json()
                error_message = f"{error_message} - {json.dumps(response_body)}"
            except:
                if hasattr(e.response, 'text'):
                    response_body = e.response.text
                    error_message = f"{error_message} - {response_body}"
        
        return {
            "success": False,
            "message": f"API request error: {error_message}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error executing create_project: {str(e)}"
        }
