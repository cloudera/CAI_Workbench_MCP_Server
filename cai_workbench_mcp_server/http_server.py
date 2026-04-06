#!/usr/bin/env python3
"""
Cloudera AI Workbench MCP HTTP Server - Simplified HTTP-only implementation
"""

import os
import json
from typing import Dict, Any
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import all the implementation functions
from .src.functions.upload_folder import upload_folder
from .src.functions.upload_file import upload_file
from .src.functions.create_job import create_job
from .src.functions.list_jobs import list_jobs
from .src.functions.delete_job import delete_job
from .src.functions.delete_all_jobs import delete_all_jobs
from .src.functions.get_project_id import get_project_id
from .src.functions.get_runtimes import get_runtimes
from .src.functions.create_job_run import create_job_run
from .src.functions.create_experiment import create_experiment
from .src.functions.create_experiment_run import create_experiment_run
from .src.functions.create_model_build import create_model_build
from .src.functions.create_model_deployment import create_model_deployment
from .src.functions.create_application import create_application
from .src.functions.list_registered_models import list_registered_models
from .src.functions.create_registered_model import create_registered_model
from .src.functions.update_registered_model import update_registered_model
from .src.functions.get_registered_model import get_registered_model
from .src.functions.delete_registered_model import delete_registered_model
from .src.functions.update_registered_model_version import update_registered_model_version
from .src.functions.get_registered_model_version import get_registered_model_version
from .src.functions.delete_registered_model_version import delete_registered_model_version
from .src.functions.create_project import create_project
from .src.functions.get_project import get_project
from .src.functions.delete_project import delete_project
from .src.functions.list_project_names import list_project_names
from .src.functions.list_project_collaborators import list_project_collaborators
from .src.functions.delete_project_collaborator import delete_project_collaborator
from .src.functions.add_project_collaborator import add_project_collaborator
from .src.functions.list_all_experiments import list_all_experiments
from .src.functions.list_experiment_runs import list_experiment_runs
from .src.functions.get_experiment_run_metrics import get_experiment_run_metrics
from .src.functions.list_all_jobs import list_all_jobs
from .src.functions.list_all_models import list_all_models
from .src.functions.create_model import create_model
from .src.functions.update_model import update_model
from .src.functions.delete_model_build import delete_model_build
from .src.functions.restart_model_deployment import restart_model_deployment
from .src.functions.download_project_file import download_project_file
from .src.functions.delete_application import delete_application
from .src.functions.delete_experiment import delete_experiment
from .src.functions.delete_experiment_run import delete_experiment_run
from .src.functions.delete_experiment_run_batch import delete_experiment_run_batch
from .src.functions.delete_model import delete_model
from .src.functions.delete_project_file import delete_project_file
from .src.functions.get_application import get_application
from .src.functions.get_experiment import get_experiment
from .src.functions.get_experiment_run import get_experiment_run
from .src.functions.get_job import get_job
from .src.functions.get_job_run import get_job_run
from .src.functions.get_model import get_model
from .src.functions.get_model_build import get_model_build
from .src.functions.get_model_deployment import get_model_deployment
from .src.functions.list_applications import list_applications
from .src.functions.list_experiments import list_experiments
from .src.functions.list_job_runs import list_job_runs
from .src.functions.list_models import list_models
from .src.functions.list_model_builds import list_model_builds
from .src.functions.list_model_deployments import list_model_deployments
from .src.functions.list_project_files import list_project_files
from .src.functions.log_experiment_run_batch import log_experiment_run_batch
from .src.functions.restart_application import restart_application
from .src.functions.stop_application import stop_application
from .src.functions.stop_job_run import stop_job_run
from .src.functions.stop_model_deployment import stop_model_deployment
from .src.functions.update_application import update_application
from .src.functions.update_experiment import update_experiment
from .src.functions.update_experiment_run import update_experiment_run
from .src.functions.update_job import update_job
from .src.functions.update_project import update_project
from .src.functions.update_project_file_metadata import update_project_file_metadata
from .src.functions.list_runtimes import list_runtimes
from .src.functions.list_runtime_addons import list_runtime_addons
from .src.functions.list_runtime_repos import list_runtime_repos
from .src.functions.create_runtime_repo import create_runtime_repo
from .src.functions.delete_runtime_repo import delete_runtime_repo
from .src.functions.update_runtime_repo import update_runtime_repo
from .src.functions.register_custom_runtime import register_custom_runtime
from .src.functions.update_runtime_status import update_runtime_status
from .src.functions.update_runtime_addon_status import update_runtime_addon_status
from .src.functions.list_docker_credentials import list_docker_credentials
from .src.functions.create_docker_credential import create_docker_credential
from .src.functions.delete_docker_credential import delete_docker_credential
from .src.functions.set_docker_credential import set_docker_credential
from .src.functions.list_v2_keys import list_v2_keys
from .src.functions.create_v2_key import create_v2_key
from .src.functions.delete_v2_key import delete_v2_key
from .src.functions.delete_v2_keys import delete_v2_keys
from .src.functions.validate_api_key import validate_api_key
from .src.functions.list_cpu_profiles import list_cpu_profiles
from .src.functions.list_groups_quota import list_groups_quota
from .src.functions.list_users_quota import list_users_quota
from .src.functions.list_teams_accelerator_quota import list_teams_accelerator_quota
from .src.functions.list_users_accelerator_quota import list_users_accelerator_quota
from .src.functions.list_usage import list_usage
from .src.functions.list_news_feeds import list_news_feeds
from .src.functions.list_ml_serving_apps import list_ml_serving_apps
from .src.functions.list_workload_executions import list_workload_executions
from .src.functions.list_workload_status import list_workload_status
from .src.functions.list_workload_types import list_workload_types
from .src.functions.get_default_quota import get_default_quota
from .src.functions.get_default_quotas import get_default_quotas
from .src.functions.list_all_resource_groups import list_all_resource_groups
from .src.functions.list_all_accelerator_node_labels import list_all_accelerator_node_labels


def get_config() -> Dict[str, str]:
    """Get configuration from Docker secrets or environment variables."""
    
    def read_secret_or_env(secret_name: str, env_var: str) -> str:
        secret_file = f"/run/secrets/{secret_name}"
        if os.path.exists(secret_file):
            with open(secret_file, 'r') as f:
                return f.read().strip()
        return os.environ.get(env_var, "")
    
    return {
        "host": read_secret_or_env("cai_workbench_host", "CAI_WORKBENCH_HOST"),
        "api_key": read_secret_or_env("cai_workbench_api_key", "CAI_WORKBENCH_API_KEY"),
        "project_id": read_secret_or_env("cai_workbench_project_id", "CAI_WORKBENCH_PROJECT_ID")
    }


# Initialize FastMCP server for HTTP
mcp = FastMCP("cloudera-ml-http")

# Complete tool implementations mapping - EXACTLY as it was working before
TOOL_IMPLEMENTATIONS = {
    # File operations
    "upload_folder_tool": lambda **p: json.dumps(upload_folder(get_config(), {
        "folder_path": p.get("folder_path"),
        "ignore_folders": p.get("ignore_folders", "").split(",") if p.get("ignore_folders") else None
    }), indent=2),
    "upload_file_tool": lambda **p: json.dumps(upload_file(get_config(), {
        "file_path": p.get("file_path"),
        "target_name": p.get("target_name"),
        "target_dir": p.get("target_dir")
    }), indent=2),
    
    # Job operations
    "create_job_tool": lambda **p: create_job(get_config(), p),
    "list_jobs_tool": lambda **p: list_jobs(get_config(), {}),
    "get_job_tool": lambda **p: json.dumps(get_job(get_config(), {
        "job_id": p.get("job_id"),
        "project_id": p.get("project_id", get_config().get("project_id", ""))
    }), indent=2),
    "update_job_tool": lambda **p: json.dumps(update_job(get_config(), p), indent=2),
    "delete_job_tool": lambda **p: delete_job(get_config(), {"job_id": p.get("job_id")}),
    "delete_all_jobs_tool": lambda **p: delete_all_jobs(get_config(), {}),
    
    # Project operations
    "get_project_id_tool": lambda **p: json.dumps(get_project_id(get_config(), {"project_name": p.get("project_name")}), indent=2),
    "list_projects_tool": lambda **p: json.dumps(get_project_id(get_config(), {"project_name": "*"}), indent=2),
    "update_project_tool": lambda **p: json.dumps(update_project(get_config(), p), indent=2),
    
    # Runtime operations
    "get_runtimes_tool": lambda **p: json.dumps(get_runtimes(get_config(), {}), indent=2),
    
    # Job run operations
    "create_job_run_tool": lambda **p: json.dumps(create_job_run(get_config(), p), indent=2),
    "list_job_runs_tool": lambda **p: json.dumps(list_job_runs(get_config(), p), indent=2),
    "get_job_run_tool": lambda **p: json.dumps(get_job_run(get_config(), p), indent=2),
    "stop_job_run_tool": lambda **p: json.dumps(stop_job_run(get_config(), p), indent=2),
    
    # Experiment operations
    "create_experiment_tool": lambda **p: json.dumps(create_experiment(get_config(), p), indent=2),
    "list_experiments_tool": lambda **p: json.dumps(list_experiments(get_config(), {
        "project_id": p.get("project_id", get_config().get("project_id", ""))
    }), indent=2),
    "get_experiment_tool": lambda **p: json.dumps(get_experiment(get_config(), p), indent=2),
    "update_experiment_tool": lambda **p: json.dumps(update_experiment(get_config(), p), indent=2),
    "delete_experiment_tool": lambda **p: json.dumps(delete_experiment(get_config(), p), indent=2),
    
    # Experiment run operations
    "create_experiment_run_tool": lambda **p: json.dumps(create_experiment_run(get_config(), p), indent=2),
    "get_experiment_run_tool": lambda **p: json.dumps(get_experiment_run(get_config(), p), indent=2),
    "update_experiment_run_tool": lambda **p: json.dumps(update_experiment_run(get_config(), p), indent=2),
    "delete_experiment_run_tool": lambda **p: json.dumps(delete_experiment_run(get_config(), p), indent=2),
    "delete_experiment_run_batch_tool": lambda **p: json.dumps(delete_experiment_run_batch(get_config(), {
        "experiment_id": p.get("experiment_id"),
        "run_ids": [run_id.strip() for run_id in p.get("run_ids", "").split(",")],
        "project_id": p.get("project_id", get_config().get("project_id", ""))
    }), indent=2),
    "log_experiment_run_batch_tool": lambda **p: json.dumps(log_experiment_run_batch(get_config(), {
        "experiment_id": p.get("experiment_id"),
        "run_updates": json.loads(p.get("run_updates", "[]")),
        "project_id": p.get("project_id", get_config().get("project_id", ""))
    }), indent=2),
    
    # Model operations
    "create_model_build_tool": lambda **p: json.dumps(create_model_build(get_config(), p), indent=2),
    "create_model_deployment_tool": lambda **p: json.dumps(create_model_deployment(get_config(), p), indent=2),
    "list_models_tool": lambda **p: json.dumps(list_models(get_config(), {
        "project_id": p.get("project_id", get_config().get("project_id", ""))
    }), indent=2),
    "list_model_builds_tool": lambda **p: json.dumps(list_model_builds(get_config(), p), indent=2),
    "list_model_deployments_tool": lambda **p: json.dumps(list_model_deployments(get_config(), p), indent=2),
    "get_model_tool": lambda **p: json.dumps(get_model(get_config(), p), indent=2),
    "get_model_build_tool": lambda **p: json.dumps(get_model_build(get_config(), p), indent=2),
    "get_model_deployment_tool": lambda **p: json.dumps(get_model_deployment(get_config(), p), indent=2),
    "stop_model_deployment_tool": lambda **p: json.dumps(stop_model_deployment(get_config(), p), indent=2),
    "delete_model_tool": lambda **p: json.dumps(delete_model(get_config(), p), indent=2),
    
    # Application operations
    "create_application_tool": lambda **p: json.dumps(create_application(get_config(), p), indent=2),
    "list_applications_tool": lambda **p: json.dumps(list_applications(get_config(), {
        "project_id": p.get("project_id", get_config().get("project_id", ""))
    }), indent=2),
    "get_application_tool": lambda **p: json.dumps(get_application(get_config(), p), indent=2),
    "update_application_tool": lambda **p: json.dumps(update_application(get_config(), p), indent=2),
    "restart_application_tool": lambda **p: json.dumps(restart_application(get_config(), p), indent=2),
    "stop_application_tool": lambda **p: json.dumps(stop_application(get_config(), p), indent=2),
    "delete_application_tool": lambda **p: json.dumps(delete_application(get_config(), p), indent=2),
    
    # File operations
    "list_project_files_tool": lambda **p: json.dumps(list_project_files(get_config(), p), indent=2),
    "delete_project_file_tool": lambda **p: json.dumps(delete_project_file(get_config(), p), indent=2),
    "update_project_file_metadata_tool": lambda **p: json.dumps(update_project_file_metadata(get_config(), p), indent=2),
}


@mcp.custom_route("/mcp-api", methods=["POST"])
async def mcp_protocol_endpoint(request):
    """Simple MCP JSON-RPC endpoint that works reliably."""
    from starlette.responses import JSONResponse
    
    try:
        data = await request.json()
        method = data.get("method", "")
        params = data.get("params", {})
        request_id = data.get("id", "unknown")
        
        if method == "initialize":
            return JSONResponse({
                "jsonrpc": "2.0", 
                "id": request_id, 
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "cloudera-ml-http",
                        "version": "1.0.0"
                    }
                }
            })
            
        elif method == "tools/list":
            # Just return the 6 main tools that were working before
            tools = [
                {"name": "list_jobs_tool", "description": "List all jobs in the Cloudera AI project", 
                 "inputSchema": {"type": "object", "properties": {"project_id": {"type": "string"}}, "required": []}},
                {"name": "list_projects_tool", "description": "List all available projects",
                 "inputSchema": {"type": "object", "properties": {}, "required": []}},
                {"name": "get_runtimes_tool", "description": "Get available runtimes from Cloudera AI",
                 "inputSchema": {"type": "object", "properties": {}, "required": []}},
                {"name": "list_applications_tool", "description": "List all applications in the Cloudera AI project",
                 "inputSchema": {"type": "object", "properties": {"project_id": {"type": "string"}}, "required": []}},
                {"name": "list_experiments_tool", "description": "List all experiments in the Cloudera AI project",
                 "inputSchema": {"type": "object", "properties": {"project_id": {"type": "string"}}, "required": []}},
                {"name": "list_models_tool", "description": "List all models in the Cloudera AI project",
                 "inputSchema": {"type": "object", "properties": {"project_id": {"type": "string"}}, "required": []}},
            ]
            return JSONResponse({"jsonrpc": "2.0", "id": request_id, "result": {"tools": tools}})
            
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            # Get implementation from our mapping
            impl_func = TOOL_IMPLEMENTATIONS.get(tool_name)
            
            if not impl_func:
                return JSONResponse({
                    "jsonrpc": "2.0", 
                    "id": request_id, 
                    "error": {"code": -32601, "message": f"Tool not found: {tool_name}"}
                }, status_code=404)
            
            try:
                result = impl_func(**arguments)
                return JSONResponse({
                    "jsonrpc": "2.0", 
                    "id": request_id, 
                    "result": {"content": [{"type": "text", "text": str(result)}], "isError": False}
                })
            except Exception as e:
                return JSONResponse({
                    "jsonrpc": "2.0", 
                    "id": request_id, 
                    "result": {"content": [{"type": "text", "text": f"Error: {str(e)}"}], "isError": True}
                })
                
        else:
            return JSONResponse({
                "jsonrpc": "2.0", 
                "id": request_id, 
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }, status_code=404)
            
    except Exception as e:
        return JSONResponse({
            "jsonrpc": "2.0", 
            "id": "server-error", 
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
        }, status_code=500)


@mcp.custom_route("/test", methods=["GET"])
async def test_endpoint(request):
    """Test endpoint to verify server is running."""
    from starlette.responses import JSONResponse
    return JSONResponse({
        "status": "ok",
        "message": "Cloudera AI HTTP Server is running",
        "transport": "http",
        "endpoint": "/mcp-api",
        "tools_available": len(TOOL_IMPLEMENTATIONS)
    })


@mcp.custom_route("/debug/tools", methods=["GET"])
async def debug_list_tools(request):
    """List all available tools."""
    from starlette.responses import JSONResponse
    return JSONResponse({
        "status": "ok",
        "tools_count": len(TOOL_IMPLEMENTATIONS),
        "tools": list(TOOL_IMPLEMENTATIONS.keys())
    })


@mcp.custom_route("/debug/call", methods=["POST"])
async def debug_call_tool(request):
    """Call a tool directly without MCP protocol."""
    from starlette.responses import JSONResponse
    
    try:
        data = await request.json()
        tool_name = data.get("tool")
        params = data.get("params", {})
        
        impl_func = TOOL_IMPLEMENTATIONS.get(tool_name)
        
        if not impl_func:
            return JSONResponse({
                "status": "error",
                "message": f"Tool '{tool_name}' not found",
                "available_tools": list(TOOL_IMPLEMENTATIONS.keys())[:10]
            }, status_code=404)
        
        result = impl_func(**params)
        
        # Try to parse as JSON if it's a string
        if isinstance(result, str):
            try:
                parsed = json.loads(result)
                return JSONResponse({
                    "status": "ok",
                    "tool": tool_name,
                    "result": parsed
                })
            except:
                return JSONResponse({
                    "status": "ok",
                    "tool": tool_name,
                    "result": result
                })
        
        return JSONResponse({
            "status": "ok",
            "tool": tool_name,
            "result": result
        })
        
    except Exception as e:
        import traceback
        return JSONResponse({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }, status_code=500)


@mcp.tool()
def create_project_tool(name: str, description: str = None, template: str = None, default_project_engine_type: str = None) -> str:
    """
    create_project tool.
    """
    config = get_config()
    
    params_dict = {}
    if name is not None:
        params_dict['name'] = name
    if description is not None:
        params_dict['description'] = description
    if template is not None:
        params_dict['template'] = template
    if default_project_engine_type is not None:
        params_dict['default_project_engine_type'] = default_project_engine_type

        
    result = create_project(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def get_project_tool(project_id: str) -> str:
    """
    get_project tool.
    """
    config = get_config()
    
    params_dict = {}
    if project_id is not None:
        params_dict['project_id'] = project_id

        
    result = get_project(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def delete_project_tool(project_id: str) -> str:
    """
    delete_project tool.
    """
    config = get_config()
    
    params_dict = {}
    if project_id is not None:
        params_dict['project_id'] = project_id

        
    result = delete_project(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def list_project_names_tool(search_filter: str = None, sort: str = None, page_size: int = None, page_token: str = None) -> str:
    """
    list_project_names tool.
    """
    config = get_config()
    
    params_dict = {}
    if search_filter is not None:
        params_dict['search_filter'] = search_filter
    if sort is not None:
        params_dict['sort'] = sort
    if page_size is not None:
        params_dict['page_size'] = page_size
    if page_token is not None:
        params_dict['page_token'] = page_token

        
    result = list_project_names(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def list_project_collaborators_tool(project_id: str, search_filter: str = None, sort: str = None, page_size: int = None, page_token: str = None) -> str:
    """
    list_project_collaborators tool.
    """
    config = get_config()
    
    params_dict = {}
    if project_id is not None:
        params_dict['project_id'] = project_id
    if search_filter is not None:
        params_dict['search_filter'] = search_filter
    if sort is not None:
        params_dict['sort'] = sort
    if page_size is not None:
        params_dict['page_size'] = page_size
    if page_token is not None:
        params_dict['page_token'] = page_token

        
    result = list_project_collaborators(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def delete_project_collaborator_tool(project_id: str, username: str) -> str:
    """
    delete_project_collaborator tool.
    """
    config = get_config()
    
    params_dict = {}
    if project_id is not None:
        params_dict['project_id'] = project_id
    if username is not None:
        params_dict['username'] = username

        
    result = delete_project_collaborator(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def add_project_collaborator_tool(project_id: str, username: str, permission: str) -> str:
    """
    add_project_collaborator tool.
    """
    config = get_config()
    
    params_dict = {}
    if project_id is not None:
        params_dict['project_id'] = project_id
    if username is not None:
        params_dict['username'] = username
    if permission is not None:
        params_dict['permission'] = permission

        
    result = add_project_collaborator(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def list_all_experiments_tool(search_filter: str = None, page_size: int = None, page_token: str = None) -> str:
    """
    list_all_experiments tool.
    """
    config = get_config()
    
    params_dict = {}
    if search_filter is not None:
        params_dict['search_filter'] = search_filter
    if page_size is not None:
        params_dict['page_size'] = page_size
    if page_token is not None:
        params_dict['page_token'] = page_token

        
    result = list_all_experiments(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def list_experiment_runs_tool(project_id: str, experiment_id: str, search_filter: str = None, page_size: int = None, page_token: str = None, sort: str = None) -> str:
    """
    list_experiment_runs tool.
    """
    config = get_config()
    
    params_dict = {}
    if project_id is not None:
        params_dict['project_id'] = project_id
    if experiment_id is not None:
        params_dict['experiment_id'] = experiment_id
    if search_filter is not None:
        params_dict['search_filter'] = search_filter
    if page_size is not None:
        params_dict['page_size'] = page_size
    if page_token is not None:
        params_dict['page_token'] = page_token
    if sort is not None:
        params_dict['sort'] = sort

        
    result = list_experiment_runs(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def get_experiment_run_metrics_tool(project_id: str, experiment_id: str, run_id: str, metric_key: str) -> str:
    """
    get_experiment_run_metrics tool.
    """
    config = get_config()
    
    params_dict = {}
    if project_id is not None:
        params_dict['project_id'] = project_id
    if experiment_id is not None:
        params_dict['experiment_id'] = experiment_id
    if run_id is not None:
        params_dict['run_id'] = run_id
    if metric_key is not None:
        params_dict['metric_key'] = metric_key

        
    result = get_experiment_run_metrics(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def list_all_jobs_tool(search_filter: str = None, page_size: int = None, page_token: str = None) -> str:
    """
    list_all_jobs tool.
    """
    config = get_config()
    
    params_dict = {}
    if search_filter is not None:
        params_dict['search_filter'] = search_filter
    if page_size is not None:
        params_dict['page_size'] = page_size
    if page_token is not None:
        params_dict['page_token'] = page_token

        
    result = list_all_jobs(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def list_all_models_tool(search_filter: str = None, page_size: int = None, page_token: str = None) -> str:
    """
    list_all_models tool.
    """
    config = get_config()
    
    params_dict = {}
    if search_filter is not None:
        params_dict['search_filter'] = search_filter
    if page_size is not None:
        params_dict['page_size'] = page_size
    if page_token is not None:
        params_dict['page_token'] = page_token

        
    result = list_all_models(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def create_model_tool(project_id: str, name: str, description: str = None, disable_authentication: bool = None) -> str:
    """
    create_model tool.
    """
    config = get_config()
    
    params_dict = {}
    if project_id is not None:
        params_dict['project_id'] = project_id
    if name is not None:
        params_dict['name'] = name
    if description is not None:
        params_dict['description'] = description
    if disable_authentication is not None:
        params_dict['disable_authentication'] = disable_authentication

        
    result = create_model(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def update_model_tool(project_id: str, model_id: str, name: str = None, description: str = None, visibility: str = None) -> str:
    """
    update_model tool.
    """
    config = get_config()
    
    params_dict = {}
    if project_id is not None:
        params_dict['project_id'] = project_id
    if model_id is not None:
        params_dict['model_id'] = model_id
    if name is not None:
        params_dict['name'] = name
    if description is not None:
        params_dict['description'] = description
    if visibility is not None:
        params_dict['visibility'] = visibility

        
    result = update_model(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def delete_model_build_tool(project_id: str, model_id: str, build_id: str) -> str:
    """
    delete_model_build tool.
    """
    config = get_config()
    
    params_dict = {}
    if project_id is not None:
        params_dict['project_id'] = project_id
    if model_id is not None:
        params_dict['model_id'] = model_id
    if build_id is not None:
        params_dict['build_id'] = build_id

        
    result = delete_model_build(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def restart_model_deployment_tool(project_id: str, model_id: str, build_id: str, deployment_id: str) -> str:
    """
    restart_model_deployment tool.
    """
    config = get_config()
    
    params_dict = {}
    if project_id is not None:
        params_dict['project_id'] = project_id
    if model_id is not None:
        params_dict['model_id'] = model_id
    if build_id is not None:
        params_dict['build_id'] = build_id
    if deployment_id is not None:
        params_dict['deployment_id'] = deployment_id

        
    result = restart_model_deployment(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def download_project_file_tool(project_id: str, path: str) -> str:
    """
    download_project_file tool.
    """
    config = get_config()
    
    params_dict = {}
    if project_id is not None:
        params_dict['project_id'] = project_id
    if path is not None:
        params_dict['path'] = path

        
    result = download_project_file(config, params_dict)
    return json.dumps(result, indent=2)


@mcp.tool()
def list_registered_models_tool(search_filter: str = None, sort: str = None, page_size: int = None, page_token: str = None) -> str:
    """
    list_registered_models tool.
    """
    config = get_config()
    
    params_dict = {}
    if search_filter is not None:
        params_dict['search_filter'] = search_filter
    if sort is not None:
        params_dict['sort'] = sort
    if page_size is not None:
        params_dict['page_size'] = page_size
    if page_token is not None:
        params_dict['page_token'] = page_token

        
    result = list_registered_models(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def create_registered_model_tool(project_id: str, experiment_id: str, run_id: str, model_path: str, model_name: str, tags: str = None, description: str = None, notes: str = None, visibility: str = None) -> str:
    """
    create_registered_model tool.
    """
    config = get_config()
    
    params_dict = {}
    if project_id is not None:
        params_dict['project_id'] = project_id
    if experiment_id is not None:
        params_dict['experiment_id'] = experiment_id
    if run_id is not None:
        params_dict['run_id'] = run_id
    if model_path is not None:
        params_dict['model_path'] = model_path
    if model_name is not None:
        params_dict['model_name'] = model_name
    if tags is not None:
        params_dict['tags'] = tags
    if description is not None:
        params_dict['description'] = description
    if notes is not None:
        params_dict['notes'] = notes
    if visibility is not None:
        params_dict['visibility'] = visibility

        
    result = create_registered_model(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def update_registered_model_tool(model_id: str, description: str = None, visibility: str = None, user_id: str = None) -> str:
    """
    update_registered_model tool.
    """
    config = get_config()
    
    params_dict = {}
    if model_id is not None:
        params_dict['model_id'] = model_id
    if description is not None:
        params_dict['description'] = description
    if visibility is not None:
        params_dict['visibility'] = visibility
    if user_id is not None:
        params_dict['user_id'] = user_id

        
    result = update_registered_model(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def get_registered_model_tool(model_id: str, search_filter: str = None, sort: str = None, page_size: int = None, page_token: str = None) -> str:
    """
    get_registered_model tool.
    """
    config = get_config()
    
    params_dict = {}
    if model_id is not None:
        params_dict['model_id'] = model_id
    if search_filter is not None:
        params_dict['search_filter'] = search_filter
    if sort is not None:
        params_dict['sort'] = sort
    if page_size is not None:
        params_dict['page_size'] = page_size
    if page_token is not None:
        params_dict['page_token'] = page_token

        
    result = get_registered_model(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def delete_registered_model_tool(model_id: str) -> str:
    """
    delete_registered_model tool.
    """
    config = get_config()
    
    params_dict = {}
    if model_id is not None:
        params_dict['model_id'] = model_id

        
    result = delete_registered_model(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def update_registered_model_version_tool(model_id: str, model_version_id: str, notes: str = None, tags: str = None) -> str:
    """
    update_registered_model_version tool.
    """
    config = get_config()
    
    params_dict = {}
    if model_id is not None:
        params_dict['model_id'] = model_id
    if model_version_id is not None:
        params_dict['model_version_id'] = model_version_id
    if notes is not None:
        params_dict['notes'] = notes
    if tags is not None:
        params_dict['tags'] = tags

        
    result = update_registered_model_version(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def get_registered_model_version_tool(model_id: str, version_id: str) -> str:
    """
    get_registered_model_version tool.
    """
    config = get_config()
    
    params_dict = {}
    if model_id is not None:
        params_dict['model_id'] = model_id
    if version_id is not None:
        params_dict['version_id'] = version_id

        
    result = get_registered_model_version(config, params_dict)
    return json.dumps(result, indent=2)

@mcp.tool()
def delete_registered_model_version_tool(model_id: str, version_id: str) -> str:
    """
    delete_registered_model_version tool.
    """
    config = get_config()
    
    params_dict = {}
    if model_id is not None:
        params_dict['model_id'] = model_id
    if version_id is not None:
        params_dict['version_id'] = version_id

        
    result = delete_registered_model_version(config, params_dict)
    return json.dumps(result, indent=2)


# --- Runtimes / credentials / global admin (same tools as stdio_server) ---
@mcp.tool()
def list_runtimes_tool(
    search_filter: str = None, sort: str = None, page_size: int = None, page_token: str = None
) -> str:
    p = {}
    if search_filter is not None:
        p["search_filter"] = search_filter
    if sort is not None:
        p["sort"] = sort
    if page_size is not None:
        p["page_size"] = page_size
    if page_token is not None:
        p["page_token"] = page_token
    return json.dumps(list_runtimes(get_config(), p), indent=2)


@mcp.tool()
def list_runtime_addons_tool(
    search_filter: str = None, sort: str = None, page_size: int = None, page_token: str = None
) -> str:
    p = {k: v for k, v in {
        "search_filter": search_filter, "sort": sort, "page_size": page_size, "page_token": page_token
    }.items() if v is not None}
    return json.dumps(list_runtime_addons(get_config(), p), indent=2)


@mcp.tool()
def list_runtime_repos_tool(
    search_filter: str = None, sort: str = None, page_size: int = None, page_token: str = None
) -> str:
    p = {k: v for k, v in {
        "search_filter": search_filter, "sort": sort, "page_size": page_size, "page_token": page_token
    }.items() if v is not None}
    return json.dumps(list_runtime_repos(get_config(), p), indent=2)


@mcp.tool()
def create_runtime_repo_tool(body_json: str) -> str:
    return json.dumps(create_runtime_repo(get_config(), {"body": json.loads(body_json)}), indent=2)


@mcp.tool()
def delete_runtime_repo_tool(runtime_repo_id: int) -> str:
    return json.dumps(delete_runtime_repo(get_config(), {"runtime_repo_id": runtime_repo_id}), indent=2)


@mcp.tool()
def update_runtime_repo_tool(runtimerepo_id: int, body_json: str) -> str:
    return json.dumps(
        update_runtime_repo(get_config(), {"runtimerepo_id": runtimerepo_id, "body": json.loads(body_json)}),
        indent=2,
    )


@mcp.tool()
def register_custom_runtime_tool(body_json: str) -> str:
    return json.dumps(register_custom_runtime(get_config(), {"body": json.loads(body_json)}), indent=2)


@mcp.tool()
def update_runtime_status_tool(body_json: str) -> str:
    return json.dumps(update_runtime_status(get_config(), {"body": json.loads(body_json)}), indent=2)


@mcp.tool()
def update_runtime_addon_status_tool(body_json: str) -> str:
    return json.dumps(update_runtime_addon_status(get_config(), {"body": json.loads(body_json)}), indent=2)


@mcp.tool()
def list_docker_credentials_tool(
    search_filter: str = None, sort: str = None, page_size: int = None, page_token: str = None
) -> str:
    p = {k: v for k, v in {
        "search_filter": search_filter, "sort": sort, "page_size": page_size, "page_token": page_token
    }.items() if v is not None}
    return json.dumps(list_docker_credentials(get_config(), p), indent=2)


@mcp.tool()
def create_docker_credential_tool(body_json: str) -> str:
    return json.dumps(create_docker_credential(get_config(), {"body": json.loads(body_json)}), indent=2)


@mcp.tool()
def delete_docker_credential_tool(docker_credential_id: str) -> str:
    return json.dumps(delete_docker_credential(get_config(), {"docker_credential_id": docker_credential_id}), indent=2)


@mcp.tool()
def set_docker_credential_tool(body_json: str) -> str:
    return json.dumps(set_docker_credential(get_config(), {"body": json.loads(body_json)}), indent=2)


@mcp.tool()
def list_v2_keys_tool(username: str) -> str:
    return json.dumps(list_v2_keys(get_config(), {"username": username}), indent=2)


@mcp.tool()
def create_v2_key_tool(username: str, body_json: str) -> str:
    return json.dumps(create_v2_key(get_config(), {"username": username, "body": json.loads(body_json)}), indent=2)


@mcp.tool()
def delete_v2_key_tool(username: str, key_id: str) -> str:
    return json.dumps(delete_v2_key(get_config(), {"username": username, "key_id": key_id}), indent=2)


@mcp.tool()
def delete_v2_keys_tool(username: str) -> str:
    return json.dumps(delete_v2_keys(get_config(), {"username": username}), indent=2)


@mcp.tool()
def validate_api_key_tool(body_json: str) -> str:
    return json.dumps(validate_api_key(get_config(), {"body": json.loads(body_json)}), indent=2)


@mcp.tool()
def list_cpu_profiles_tool(
    search_filter: str = None, sort: str = None, page_size: int = None, page_token: str = None
) -> str:
    p = {k: v for k, v in {
        "search_filter": search_filter, "sort": sort, "page_size": page_size, "page_token": page_token
    }.items() if v is not None}
    return json.dumps(list_cpu_profiles(get_config(), p), indent=2)


@mcp.tool()
def list_groups_quota_tool(
    search_filter: str = None, sort: str = None, page_size: int = None, page_token: str = None
) -> str:
    p = {k: v for k, v in {
        "search_filter": search_filter, "sort": sort, "page_size": page_size, "page_token": page_token
    }.items() if v is not None}
    return json.dumps(list_groups_quota(get_config(), p), indent=2)


@mcp.tool()
def list_users_quota_tool(
    search_filter: str = None, sort: str = None, page_size: int = None, page_token: str = None
) -> str:
    p = {k: v for k, v in {
        "search_filter": search_filter, "sort": sort, "page_size": page_size, "page_token": page_token
    }.items() if v is not None}
    return json.dumps(list_users_quota(get_config(), p), indent=2)


@mcp.tool()
def list_teams_accelerator_quota_tool(search_filter: str = None) -> str:
    p = {}
    if search_filter is not None:
        p["search_filter"] = search_filter
    return json.dumps(list_teams_accelerator_quota(get_config(), p), indent=2)


@mcp.tool()
def list_users_accelerator_quota_tool(search_filter: str = None) -> str:
    p = {}
    if search_filter is not None:
        p["search_filter"] = search_filter
    return json.dumps(list_users_accelerator_quota(get_config(), p), indent=2)


@mcp.tool()
def list_usage_tool(
    search_filter: str = None,
    sort: str = None,
    page_size: int = None,
    page_token: str = None,
    multi_column_search_filter: str = None,
    time_range_search_filter: str = None,
) -> str:
    p = {k: v for k, v in {
        "search_filter": search_filter,
        "sort": sort,
        "page_size": page_size,
        "page_token": page_token,
        "multi_column_search_filter": multi_column_search_filter,
        "time_range_search_filter": time_range_search_filter,
    }.items() if v is not None}
    return json.dumps(list_usage(get_config(), p), indent=2)


@mcp.tool()
def list_news_feeds_tool(category: str, page_size: int = None, page_token: str = None) -> str:
    p = {"category": category}
    if page_size is not None:
        p["page_size"] = page_size
    if page_token is not None:
        p["page_token"] = page_token
    return json.dumps(list_news_feeds(get_config(), p), indent=2)


@mcp.tool()
def list_ml_serving_apps_tool(force_refresh: bool = None) -> str:
    p = {}
    if force_refresh is not None:
        p["force_refresh"] = force_refresh
    return json.dumps(list_ml_serving_apps(get_config(), p), indent=2)


@mcp.tool()
def list_workload_executions_tool(
    search_filter: str = None,
    page_size: int = None,
    page_token: str = None,
    sort: str = None,
    multi_column_search_filter: str = None,
    time_range_search_filter: str = None,
) -> str:
    p = {k: v for k, v in {
        "search_filter": search_filter,
        "page_size": page_size,
        "page_token": page_token,
        "sort": sort,
        "multi_column_search_filter": multi_column_search_filter,
        "time_range_search_filter": time_range_search_filter,
    }.items() if v is not None}
    return json.dumps(list_workload_executions(get_config(), p), indent=2)


@mcp.tool()
def list_workload_status_tool() -> str:
    return json.dumps(list_workload_status(get_config(), {}), indent=2)


@mcp.tool()
def list_workload_types_tool() -> str:
    return json.dumps(list_workload_types(get_config(), {}), indent=2)


@mcp.tool()
def get_default_quota_tool(uuid: str = None) -> str:
    p = {}
    if uuid is not None:
        p["uuid"] = uuid
    return json.dumps(get_default_quota(get_config(), p), indent=2)


@mcp.tool()
def get_default_quotas_tool(uuid: str = None) -> str:
    p = {}
    if uuid is not None:
        p["uuid"] = uuid
    return json.dumps(get_default_quotas(get_config(), p), indent=2)


@mcp.tool()
def list_all_resource_groups_tool() -> str:
    return json.dumps(list_all_resource_groups(get_config(), {}), indent=2)


@mcp.tool()
def list_all_accelerator_node_labels_tool() -> str:
    return json.dumps(list_all_accelerator_node_labels(get_config(), {}), indent=2)


def main():
    """Run the HTTP server."""
    config = get_config()
    
    # Check configuration
    if not config.get("host") or not config.get("api_key"):
        print("Error: Missing required configuration")
        print("Please set CAI_WORKBENCH_HOST and CAI_WORKBENCH_API_KEY")
        return
    
    # Get host and port from environment or use defaults
    host = os.getenv("CAI_MCP_HOST", "0.0.0.0")
    port = int(os.getenv("CAI_MCP_PORT", "8000"))
    
    print("Starting Cloudera AI HTTP Server...")
    print(f"Connected to: {config['host']}")
    print(f"Tools available: {len(TOOL_IMPLEMENTATIONS)}")
    print(f"Server will start on {host}:{port}")
    print("")
    print("Endpoints:")
    print(f"  - MCP Protocol: http://localhost:{port}/mcp-api")
    print(f"  - Debug tools:  http://localhost:{port}/debug/tools")
    print(f"  - Debug call:   http://localhost:{port}/debug/call")
    print(f"  - Test status:  http://localhost:{port}/test")
    print("")
    print("⚠️  WARNING: No authentication - development use only!")
    
    # Run HTTP server
    mcp.run(transport="http", host=host, port=port)


if __name__ == "__main__":
    main()
