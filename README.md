# Cloudera AI Workbench MCP Server

A Model Context Protocol (MCP) server for Cloudera AI workbench built with FastMCP, enabling LLMs to interact with Cloudera AI Workbench APIs.

## Features

### Cloudera AI Integration
- **File Management**: Upload files and folders with directory structure preservation
- **Job Management**: Create, run, monitor, and delete jobs
- **Model Lifecycle**: Build, deploy, and manage ML models
- **Experiment Tracking**: Log metrics, parameters, and manage experiment runs
- **Project Operations**: Project discovery, file listing, and metadata management
- **Application Management**: Create, update, and manage applications

### Transport Modes
1. **STDIO** (Recommended): Secure subprocess communication for local/Claude Desktop use
2. **HTTP**: Simple HTTP API for development/testing (no authentication)

## Prerequisites
- Python 3.10 or higher
- Access to a Cloudera AI instance  
- Valid Cloudera AI API key
- `uv` package manager (for local development)

## Quick Start

### Option 1: Cloudera AI Environment(Agent Studio)

The easiest way to use this MCP server is through [Cloudera Agent Studio](https://docs.cloudera.com/machine-learning/cloud/use-ai-studios/topics/ml-agent-studio-overview.html), which provides a managed environment for AI agents.

#### Setup 

1. **Navigate to Agent Studio** in your Cloudera AI workspace
2. **Add MCP Server** in the configuration:

```json
{
  "mcpServers": {
    "cloudera-ai": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/cloudera/CAI_Workbench_MCP_Server.git",
        "cai-workbench-mcp-stdio"
      ],
      "env": {
        "CAI_WORKBENCH_HOST": "${CAI_WORKBENCH_HOST}",
        "CAI_WORKBENCH_API_KEY": "${CAI_WORKBENCH_API_KEY}",
        "CAI_WORKBENCH_PROJECT_ID": "${CAI_WORKBENCH_PROJECT_ID}"
      }
    }
  }
}
```

3. **Set environment variables** in Agent Studio settings:
   - `CAI_WORKBENCH_HOST`: Your Cloudera AI instance URL (e.g., `https://ml-xxxx.cloudera.site`)
   - `CAI_WORKBENCH_API_KEY`: Your API key from Cloudera AI
   - `CAI_WORKBENCH_PROJECT_ID`: Your default project ID (optional)

4. **Save and test** - Your agent now has access to all **105** Cloudera AI workbench tools (use MCP `tools/list` for the current list).




### Option 2: Docker

Configure your Cloudera AI domain first - see [SETUP.md](./SETUP.md).

```bash
# Clone repository
git clone https://github.com/cloudera/CAI_Workbench_MCP_Server.git
cd CAI_Workbench_MCP_Server

# Configure your CAI domain in Makefile
# Build and test
make build
make test
make run
```

See [DOCKER.md](./DOCKER.md) for Docker documentation.

### Option 4: Local Development

#### 1. Clone and setup
```bash
git clone https://github.com/cloudera/CAI_Workbench_MCP_Server.git
cd CAI_Workbench_MCP_Server
uv sync
```

#### 2. Install Cloudera AI API Client
```bash
# Set your Cloudera AI domain
export CDSW_DOMAIN="ml-xxxx.cloudera.site"  # Replace with your actual domain

# Install cmlapi from your Cloudera AI instance
uv pip install https://$CDSW_DOMAIN/api/v2/python.tar.gz
```

#### 3. Configure Environment Variables
Create a `.env` file or export:

```bash
# Required
export CAI_WORKBENCH_HOST="https://ml-xxxx.cloudera.site"
export CAI_WORKBENCH_API_KEY="your-api-key"

# Optional  
export CAI_WORKBENCH_PROJECT_ID="your-default-project-id"
```

## Usage

### STDIO Mode (Recommended)

Best for Claude Desktop and secure local usage:

```bash
# Run the STDIO server
uv run -m cai_workbench_mcp_server.stdio_server

# Or use the shortcut
uvx --from . cai-workbench-mcp-stdio
```

#### Configure Claude Desktop

Add to your Claude Desktop configuration:

**Secure (Docker Secrets - Recommended):**
```json
{
  "mcpServers": {
    "cai_workbench_mcp": {
      "command": "docker-compose",
      "args": [
        "-f", 
        "/absolute/path/to/cai_workbench_mcp_server/docker-compose.secrets.yml",
        "run", "--rm", "cai-workbench-mcp-server"
      ]
    }
  }
}
```

**Simple (Environment Variables):**
```json
{
  "mcpServers": {
    "cai_workbench_mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "CAI_WORKBENCH_HOST=https://your-instance.site",
        "-e", "CAI_WORKBENCH_API_KEY=your-api-key",
        "cai-workbench-mcp-server"
      ]
    }
  }
}
```

### HTTP Mode (Development Only)

⚠️ **Warning**: HTTP mode runs without authentication - use only for local development!

```bash
# Start HTTP server on port 8000
uv run -m cai_workbench_mcp_server.http_server

# Or use the shortcut
uvx --from . cai-workbench-mcp-http
```

#### Available Endpoints

1. **MCP Protocol Endpoint**: `/mcp-api` (simplified MCP protocol)
   ```bash
   # List tools
   curl -X POST http://localhost:8000/mcp-api \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}'
   
   # Call a tool
   curl -X POST http://localhost:8000/mcp-api \
     -H "Content-Type: application/json" \
     -d '{
       "jsonrpc": "2.0", 
       "id": "2", 
       "method": "tools/call",
       "params": {
         "name": "list_projects_tool",
         "arguments": {}
       }
     }'
   ```

2. **Debug Endpoints** (bypass MCP protocol):
   ```bash
   # Test server status
   curl http://localhost:8000/test
   
   # List all tools
   curl http://localhost:8000/debug/tools
   
   # Call any tool directly
   curl -X POST http://localhost:8000/debug/call \
     -H "Content-Type: application/json" \
     -d '{"tool": "list_projects_tool", "params": {}}'
   ```

#### Client Connection Examples

Using MCP clients:
```bash
# FastMCP client
cloudera-mcp chat http-stateless http://localhost:8000/mcp-api

# Python client
from fastmcp import Client
client = Client("http://localhost:8000/mcp-api")
```

## Available Tools (105 total)

The server exposes **105** tools. The authoritative list is whatever the running server returns from MCP `tools/list` or `GET /debug/tools`. Below is a grouped overview (not every tool is listed).

### Project management
- `list_projects_tool`, `get_project_id_tool`, `update_project_tool`
- `create_project_tool`, `get_project_tool`, `delete_project_tool`, `list_project_names_tool`
- `list_project_collaborators_tool`, `add_project_collaborator_tool`, `delete_project_collaborator_tool`

### File operations
- `upload_file_tool`, `upload_folder_tool`, `list_project_files_tool`, `delete_project_file_tool`, `update_project_file_metadata_tool`, `download_project_file_tool`

### Jobs
- `create_job_tool`, `list_jobs_tool`, `get_job_tool`, `update_job_tool`, `delete_job_tool`, `delete_all_jobs_tool`
- `create_job_run_tool`, `list_job_runs_tool`, `get_job_run_tool`, `stop_job_run_tool`
- Workspace-wide: `list_all_jobs_tool`

### Models (deployments & builds)
- `list_models_tool`, `get_model_tool`, `delete_model_tool`, `create_model_tool`, `update_model_tool`
- `create_model_build_tool`, `list_model_builds_tool`, `get_model_build_tool`, `delete_model_build_tool`
- `create_model_deployment_tool`, `list_model_deployments_tool`, `get_model_deployment_tool`, `stop_model_deployment_tool`, `restart_model_deployment_tool`
- Workspace-wide: `list_all_models_tool`

### Model registry (MLflow-linked)
- `list_registered_models_tool`, `create_registered_model_tool`, `get_registered_model_tool`, `update_registered_model_tool`, `delete_registered_model_tool`
- `update_registered_model_version_tool`, `get_registered_model_version_tool`, `delete_registered_model_version_tool`

For `create_registered_model_tool`, **`tags`** is passed through the MCP as a string. Use a **JSON array** string, for example `[{"key":"env","value":"prod"}]`, so the payload matches the API.

### Experiments
- Per-project: `create_experiment_tool`, `list_experiments_tool`, `get_experiment_tool`, `update_experiment_tool`, `delete_experiment_tool`
- Runs: `create_experiment_run_tool`, `get_experiment_run_tool`, `update_experiment_run_tool`, `delete_experiment_run_tool`, `delete_experiment_run_batch_tool`, `log_experiment_run_batch_tool`
- Workspace-wide: `list_all_experiments_tool`, `list_experiment_runs_tool`, `get_experiment_run_metrics_tool`

### Applications
- `create_application_tool`, `list_applications_tool`, `get_application_tool`, `update_application_tool`, `restart_application_tool`, `stop_application_tool`, `delete_application_tool`

### Runtimes, repos, Docker, API keys
- `get_runtimes_tool`, `list_runtimes_tool`, `list_runtime_addons_tool`, `list_runtime_repos_tool`, `create_runtime_repo_tool`, `delete_runtime_repo_tool`, `update_runtime_repo_tool`
- `register_custom_runtime_tool`, `update_runtime_status_tool`, `update_runtime_addon_status_tool`
- `list_docker_credentials_tool`, `create_docker_credential_tool`, `delete_docker_credential_tool`, `set_docker_credential_tool`
- `list_v2_keys_tool`, `create_v2_key_tool`, `delete_v2_key_tool`, `delete_v2_keys_tool`, `validate_api_key_tool`

### Quotas, workload, platform
- `list_cpu_profiles_tool`, `list_groups_quota_tool`, `list_users_quota_tool`, `list_teams_accelerator_quota_tool`, `list_users_accelerator_quota_tool`, `list_usage_tool`
- `get_default_quota_tool`, `get_default_quotas_tool`, `list_all_resource_groups_tool`, `list_all_accelerator_node_labels_tool`
- `list_news_feeds_tool`, `list_ml_serving_apps_tool`, `list_workload_executions_tool`, `list_workload_status_tool`, `list_workload_types_tool`

### Optional sample script (MLflow / XGBoost)

`inference_test.py` at the repository root is an **optional** end-to-end sample: train a small XGBoost model, log it with MLflow (experiment `xgboost-mcp`), and optionally register via the registry. It is **not** part of the MCP package dependencies. Install extras locally, for example: `uv pip install mlflow xgboost scikit-learn`. Runs inside a Cloudera AI workbench session work without extra tracking URI setup; from a laptop you must align `MLFLOW_TRACKING_URI` / auth with your environment.

## Examples

### Upload and Run a Job

```python
# 1. Upload your script
upload_file_tool(
    file_path="train.py",
    target_dir="scripts/"
)

# 2. Create a job
create_job_tool(
    name="Model Training",
    script="scripts/train.py",
    cpu=2,
    memory=4,
    runtime_identifier="python3.9-standard"
)

# 3. Run the job
create_job_run_tool(
    project_id="your-project-id",
    job_id="created-job-id"
)
```

### Deploy a Model

```python
# 1. Create model build
create_model_build_tool(
    project_id="your-project-id",
    model_id="your-model-id",
    file_path="model.py",
    function_name="predict"
)

# 2. Deploy the model
create_model_deployment_tool(
    project_id="your-project-id",
    model_id="your-model-id", 
    build_id="created-build-id",
    name="Production Deployment"
)
```

## Troubleshooting

1. **"Missing required configuration"**: Set CAI_WORKBENCH_HOST and CAI_WORKBENCH_API_KEY
2. **"cmlapi not found"**: Install from your Cloudera AI instance
3. **HTTP connection issues**: Ensure server is running on correct port
4. **Tool not found**: Check tool name spelling (use `list_tools`)

## Security Notes

- **STDIO Mode**: Secure - credentials in environment variables
- **HTTP Mode**: No authentication - development only!
- **Production**: Always use STDIO mode or deploy with proper security

## Related Resources

- [Cloudera AI Workbench](https://docs.cloudera.com/machine-learning/1.5.5/workspaces-privatecloud/topics/ml-pvc-provision-ml-workspace.html) - Cloudera AI documentation
- [FastMCP](https://gofastmcp.com/) - The MCP framework
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP specification

---

## Legal Notice

**IMPORTANT: Please read the following before proceeding.**

Cloudera, Inc. ("Cloudera") makes available to you this optional software, which may include accelerators for machine learning projects ("AMPs"), Hugging Face Spaces, or AI models, constitutes reference machine learning projects ("Reference Projects"). By configuring and launching this Reference Project, you acknowledge and assume the risk that using Reference Projects may (i) cause third party software, such as third-party large language models, to be downloaded directly into your environment and/or (ii) enable third-party services, such as third-party AI services, and transmission of data and metadata to such third-party services providers. Any such third-party software is not validated or maintained by Cloudera. Any support provided for Reference Projects is at Cloudera's sole discretion. You agree to comply with any applicable license terms or terms of use, including any third-party license terms, for Reference Projects.

If you do not wish to download and install the third party software packages, do not configure, launch or otherwise use this Reference Project. By configuring, launching or otherwise using the Reference Project, you acknowledge the foregoing statement and agree that Cloudera is not responsible or liable in any way for any third party software packages.

*Copyright (c) 2025 - Cloudera, Inc. All rights reserved.*

