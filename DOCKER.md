# Docker Guide

## Prerequisites

- Docker installed and running
- Access to your Cloudera AI instance

## Quick Start

### 1. Set Environment Variable

```bash
# Set your Cloudera AI host
export CAI_WORKBENCH_HOST=https://your-cai-instance.cloudera.site
```

### 2. Build and Run

```bash
# Build the image
make build

# Test it works
make test

# Run for Claude Desktop (STDIO mode)
make run
```

## Claude Desktop Configuration

**Recommended (Docker Secrets):**
```json
{
  "mcpServers": {
    "cai_workbench": {
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

**Alternative (Environment Variables):**
```json
{
  "mcpServers": {
    "cai_workbench": {
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

## Using Docker Secrets (Secure)

For production use, avoid environment variables by using Docker secrets:

### Setup Secrets

```bash
# Create secrets directory
mkdir -p secrets

# Add your credentials (these files are not committed to git)
echo "https://your-cai-instance.cloudera.site" > secrets/cai_workbench_host
echo "your-api-key-here" > secrets/cai_workbench_api_key
echo "your-project-id" > secrets/cai_workbench_project_id

# Secure the files
chmod 600 secrets/*
```

### Build and Run with Secrets

```bash
# Build (still needs CAI_WORKBENCH_HOST for cmlapi installation)
export CAI_WORKBENCH_HOST=https://your-cai-instance.cloudera.site
make build

# Run with secrets
make run-secrets
```

### Claude Desktop Configuration (Secrets)

```json
{
  "mcpServers": {
    "cai_workbench": {
      "command": "docker-compose",
      "args": [
        "-f", 
        "/absolute/path/to/cai_workbench_mcp_server/docker-compose.secrets.yml", 
        "run", 
        "--rm", 
        "cai-workbench-mcp-server"
      ]
    }
  }
}
```

## Commands

| Command | Description |
|---------|-------------|
| `make build` | Build Docker image |
| `make run` | Run STDIO mode (env vars) |
| `make run-secrets` | Run STDIO mode (Docker secrets) |
| `make test` | Test STDIO transport |
| `make clean` | Remove image |


## Troubleshooting

### Module not found errors
- Check that your CAI_DOMAIN is correct in the Makefile
- Ensure your CAI instance is accessible

### Claude Desktop connection issues
- Make sure you're using STDIO mode (`make run`)
- Verify environment variables in Claude config
- Rebuild the image if you updated from an older version