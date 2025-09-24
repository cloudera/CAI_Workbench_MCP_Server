# Setup Guide

## Required Configuration

Set the `CLOUDERA_ML_HOST` environment variable before building.

### Step 1: Set Environment Variable

```bash
# Set your Cloudera ML host URL
export CLOUDERA_ML_HOST=https://your-cml-instance.cloudera.site
```

### Step 2: Build and Test

```bash
# Build the Docker image
make build

# Test the implementation
make test

# Run for Claude Desktop
make run
```

## Environment Variables

For the server to connect to CML, set these environment variables:

- `CLOUDERA_ML_HOST` - Full URL to your CML instance (https://your-domain.com)
- `CLOUDERA_ML_API_KEY` - Your CML API key
- `CLOUDERA_ML_PROJECT_ID` - Your project ID (optional)

## Claude Desktop Setup

1. Configure your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "cml": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "cml-mcp-server"],
      "env": {
        "CLOUDERA_ML_HOST": "https://your-cml-domain.com",
        "CLOUDERA_ML_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

2. Restart Claude Desktop

## Common Issues

**Build fails with "No module named 'cmlapi'"**
- Your CML_DOMAIN is incorrect or unreachable
- Check network connectivity to your CML instance

**Claude Desktop shows JSON parse errors**  
- Make sure you built the latest Docker image after fixes
- Use STDIO mode, not HTTP mode for Claude Desktop

**API authentication errors**
- Check your CLOUDERA_ML_API_KEY is valid
- Verify CLOUDERA_ML_HOST includes https:// prefix