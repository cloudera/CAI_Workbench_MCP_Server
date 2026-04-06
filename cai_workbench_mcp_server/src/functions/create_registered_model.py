"""Register a model. function for Cloudera AI Workbench MCP"""

import requests
import json
from typing import Dict, Any

def create_registered_model(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Register a model.
    
    Args:
        config: MCP configuration with host and api_key
        params: Function parameters
            - project_id (required)
            - experiment_id (required)
            - run_id (required)
            - model_path (required)
            - model_name (required)
            - tags (optional)
            - description (optional)
            - notes (optional)
            - visibility (optional)
        
    Returns:
        create_registered_model results
    """
    try:
        # Validate required parameters
        required_params = ['project_id', 'experiment_id', 'run_id', 'model_path', 'model_name']
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
        payload["project_id"] = params["project_id"]
        payload["experiment_id"] = params["experiment_id"]
        payload["run_id"] = params["run_id"]
        payload["model_path"] = params["model_path"]
        payload["model_name"] = params["model_name"]
        if "tags" in params and params["tags"] is not None:
            t = params["tags"]
            if isinstance(t, str):
                try:
                    payload["tags"] = json.loads(t)
                except json.JSONDecodeError:
                    return {
                        "success": False,
                        "message": "tags must be a JSON array string, e.g. "
                        '\'[{"key":"k","value":"v"}]\'',
                    }
            else:
                payload["tags"] = t
        if "description" in params:
            payload["description"] = params["description"]
        if "notes" in params:
            payload["notes"] = params["notes"]
        if "visibility" in params:
            payload["visibility"] = params["visibility"]

        
        # Build the URL for the request
        api_url = f"{host}/api/v2/registry/models"

        
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
            "message": "Successfully executed create_registered_model",
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
            "message": f"Error executing create_registered_model: {str(e)}"
        }
