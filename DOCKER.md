# Docker Guide

## Prerequisites

- Docker installed and running
- Access to your Cloudera ML instance

## Quick Start

### 1. Set Environment Variable

```bash
# Set your Cloudera ML host
export CLOUDERA_ML_HOST=https://your-cml-instance.cloudera.site
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
    "cml": {
      "command": "docker-compose",
      "args": [
        "-f", 
        "/absolute/path/to/cml_mcp_server/docker-compose.secrets.yml",
        "run", "--rm", "cml-mcp-server"
      ]
    }
  }
}
```

**Alternative (Environment Variables):**
```json
{
  "mcpServers": {
    "cml": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "CLOUDERA_ML_HOST=https://your-instance.site",
        "-e", "CLOUDERA_ML_API_KEY=your-api-key",
        "cml-mcp-server"
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
echo "https://your-cml-instance.cloudera.site" > secrets/cloudera_ml_host
echo "your-api-key-here" > secrets/cloudera_ml_api_key
echo "your-project-id" > secrets/cloudera_ml_project_id

# Secure the files
chmod 600 secrets/*
```

### Build and Run with Secrets

```bash
# Build (still needs CLOUDERA_ML_HOST for cmlapi installation)
export CLOUDERA_ML_HOST=https://your-cml-instance.cloudera.site
make build

# Run with secrets
make run-secrets
```

### Claude Desktop Configuration (Secrets)

```json
{
  "mcpServers": {
    "cml": {
      "command": "docker-compose",
      "args": [
        "-f", 
        "/absolute/path/to/cml_mcp_server/docker-compose.secrets.yml", 
        "run", 
        "--rm", 
        "cml-mcp-server"
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
- Check that your CML_DOMAIN is correct in the Makefile
- Ensure your CML instance is accessible

### Claude Desktop connection issues
- Make sure you're using STDIO mode (`make run`)
- Verify environment variables in Claude config
- Rebuild the image if you updated from an older version