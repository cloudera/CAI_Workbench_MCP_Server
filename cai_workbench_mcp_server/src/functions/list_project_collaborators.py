"""List project collaborators. function for Cloudera AI Workbench MCP"""

import requests
import json
from typing import Dict, Any

def list_project_collaborators(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    List project collaborators.
    
    Args:
        config: MCP configuration with host and api_key
        params: Function parameters
            - project_id (required)
            - search_filter (optional)
            - sort (optional)
            - page_size (optional)
            - page_token (optional)
        
    Returns:
        list_project_collaborators results
    """
    try:
        # Validate required parameters
        required_params = ['project_id']
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
            

        
        # Build the URL for the request
        api_url = f"{host}/api/v2/projects/{params['project_id']}/collaborators"
        # Add query parameters
        query_params = []
        if "search_filter" in params and params["search_filter"]:
            query_params.append(f"search_filter={params['search_filter']}")
        if "sort" in params and params["sort"]:
            query_params.append(f"sort={params['sort']}")
        if "page_size" in params and params["page_size"]:
            query_params.append(f"page_size={params['page_size']}")
        if "page_token" in params and params["page_token"]:
            query_params.append(f"page_token={params['page_token']}")
        if query_params:
            api_url += "?" + "&".join(query_params)

        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Make the request
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        # Parse the response
        try:
            data = response.json()
        except:
            data = {"message": "Success", "text": response.text}
        
        return {
            "success": True,
            "message": "Successfully executed list_project_collaborators",
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
            "message": f"Error executing list_project_collaborators: {str(e)}"
        }
