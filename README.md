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

4. **Save and test** - Your agent now has access to all 47 Cloudera AI workbench tools!




### Option 2: Docker

Configure your Cloudera AI domain first - see [SETUP.md](./SETUP.md).

```bash
# Clone repository
git clone https://github.com/cloudera/CAI_Workbench_MCP_Server.git
cd cai_workbench_mcp_server

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
cd cai_workbench_mcp_server
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

## Available Tools (47 total)

### Project Management
- `list_projects_tool` - List all available projects
- `get_project_id_tool` - Get project ID from name
- `update_project_tool` - Update project settings

### File Operations
- `upload_file_tool` - Upload single file
- `upload_folder_tool` - Upload entire folder
- `list_project_files_tool` - List files in project
- `delete_project_file_tool` - Delete file/directory

### Job Management
- `create_job_tool` - Create new job
- `list_jobs_tool` - List all jobs
- `get_job_tool` - Get job details
- `update_job_tool` - Update job configuration
- `delete_job_tool` - Delete a job
- `create_job_run_tool` - Run a job
- `list_job_runs_tool` - List job runs
- `get_job_run_tool` - Get run details
- `stop_job_run_tool` - Stop running job

### Model Management
- `list_models_tool` - List all models
- `get_model_tool` - Get model details
- `create_model_build_tool` - Build a model
- `list_model_builds_tool` - List model builds
- `get_model_build_tool` - Get build details
- `create_model_deployment_tool` - Deploy a model
- `list_model_deployments_tool` - List deployments
- `get_model_deployment_tool` - Get deployment details
- `stop_model_deployment_tool` - Stop deployment
- `delete_model_tool` - Delete a model

### Experiment Tracking
- `create_experiment_tool` - Create experiment
- `list_experiments_tool` - List experiments
- `get_experiment_tool` - Get experiment details
- `update_experiment_tool` - Update experiment
- `delete_experiment_tool` - Delete experiment
- `create_experiment_run_tool` - Create run
- `get_experiment_run_tool` - Get run details
- `update_experiment_run_tool` - Update run
- `delete_experiment_run_tool` - Delete run
- `log_experiment_run_batch_tool` - Log batch metrics

### Application Management
- `create_application_tool` - Create application
- `list_applications_tool` - List applications
- `get_application_tool` - Get app details
- `update_application_tool` - Update app
- `restart_application_tool` - Restart app
- `stop_application_tool` - Stop app
- `delete_application_tool` - Delete app

### System Information
- `get_runtimes_tool` - Get available ML runtimes

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

