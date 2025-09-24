#!/usr/bin/env python3
"""
Cloudera ML MCP HTTP Server - Simplified HTTP-only implementation
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


def get_config() -> Dict[str, str]:
    """Get configuration from Docker secrets or environment variables."""
    
    def read_secret_or_env(secret_name: str, env_var: str) -> str:
        secret_file = f"/run/secrets/{secret_name}"
        if os.path.exists(secret_file):
            with open(secret_file, 'r') as f:
                return f.read().strip()
        return os.environ.get(env_var, "")
    
    return {
        "host": read_secret_or_env("cloudera_ml_host", "CLOUDERA_ML_HOST"),
        "api_key": read_secret_or_env("cloudera_ml_api_key", "CLOUDERA_ML_API_KEY"),
        "project_id": read_secret_or_env("cloudera_ml_project_id", "CLOUDERA_ML_PROJECT_ID")
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
                {"name": "list_jobs_tool", "description": "List all jobs in the Cloudera ML project", 
                 "inputSchema": {"type": "object", "properties": {"project_id": {"type": "string"}}, "required": []}},
                {"name": "list_projects_tool", "description": "List all available projects",
                 "inputSchema": {"type": "object", "properties": {}, "required": []}},
                {"name": "get_runtimes_tool", "description": "Get available runtimes from Cloudera ML",
                 "inputSchema": {"type": "object", "properties": {}, "required": []}},
                {"name": "list_applications_tool", "description": "List all applications in the Cloudera ML project",
                 "inputSchema": {"type": "object", "properties": {"project_id": {"type": "string"}}, "required": []}},
                {"name": "list_experiments_tool", "description": "List all experiments in the Cloudera ML project",
                 "inputSchema": {"type": "object", "properties": {"project_id": {"type": "string"}}, "required": []}},
                {"name": "list_models_tool", "description": "List all models in the Cloudera ML project",
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
        "message": "Cloudera ML HTTP Server is running",
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


def main():
    """Run the HTTP server."""
    config = get_config()
    
    # Check configuration
    if not config.get("host") or not config.get("api_key"):
        print("Error: Missing required configuration")
        print("Please set CLOUDERA_ML_HOST and CLOUDERA_ML_API_KEY")
        return
    
    # Get host and port from environment or use defaults
    host = os.getenv("CML_MCP_HOST", "0.0.0.0")
    port = int(os.getenv("CML_MCP_PORT", "8000"))
    
    print("Starting Cloudera ML HTTP Server...")
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
