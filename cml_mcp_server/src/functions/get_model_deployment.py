"""Get model deployment function for Cloudera AI Workbench MCP"""

import os
import json
import requests
from urllib.parse import urlparse
from typing import Dict, Any


def get_model_deployment(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get details of a specific model deployment from Cloudera AI
    
    Args:
        config (dict): MCP configuration containing host and api_key
        params (dict): Parameters for API call
            - model_id (str): ID of the model
            - deployment_id (str): ID of the deployment to retrieve
            - project_id (str): ID of the project containing the model
    
    Returns:
        dict: Response containing model deployment details or error message
    """
    # Validate parameters
    if 'model_id' not in params:
        return {
            'success': False,
            'message': 'Model ID is required'
        }
    
    if 'deployment_id' not in params:
        return {
            'success': False,
            'message': 'Deployment ID is required'
        }
    
    model_id = params['model_id']
    deployment_id = params['deployment_id']
    
    # Check if project_id is in params or config
    if 'project_id' not in params and 'project_id' not in config:
        return {
            'success': False,
            'message': 'Project ID is required but not provided in parameters or configuration'
        }
    
    project_id = params.get('project_id', config.get('project_id', ''))
    
    # Format host URL
    host = config['host']
    parsed_url = urlparse(host)
    
    # Ensure the URL has the correct scheme
    if not parsed_url.scheme:
        host = f"https://{host}"
    elif host.startswith('https://https://'):
        host = host.replace('https://https://', 'https://')
    
    # Construct API URL
    api_url = f"{host}/api/v1/projects/{project_id}/models/{model_id}/deployments/{deployment_id}"
    
    # Set up headers
    headers = {
        'Authorization': f'Bearer {config["api_key"]}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Make GET request
        response = requests.get(api_url, headers=headers, timeout=30)
        
        # Check if request was successful
        if response.status_code >= 400:
            return {
                'success': False,
                'message': f'Failed to get model deployment: HTTP {response.status_code}',
                'error': response.text
            }
        
        # Parse the response
        try:
            response_data = response.json()
            return {
                'success': True,
                'data': response_data
            }
        except json.JSONDecodeError:
            return {
                'success': False,
                'message': f'Invalid JSON response: {response.text}'
            }
    
    except requests.RequestException as e:
        return {
            'success': False,
            'message': f'Error getting model deployment: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error getting model deployment: {str(e)}'
        } 