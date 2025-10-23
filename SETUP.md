# Setup Guide

## Required Configuration

Set the `CAI_WORKBENCH_HOST` environment variable before building.

### Step 1: Set Environment Variable

```bash
# Set your Cloudera ML host URL
export CAI_WORKBENCH_HOST=https://your-cai-instance.cloudera.site
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

For the server to connect to CAI, set these environment variables:

- `CAI_WORKBENCH_HOST` - Full URL to your CAI workbench instance (https://your-domain.com)
- `CAI_WORKBENCH_API_KEY` - Your CAI API key
- `CAI_WORKBENCH_PROJECT_ID` - Your project ID (optional)

## Claude Desktop Setup

1. Configure your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "cai_workbench_mcp": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "cai-workbench-mcp-server"],
      "env": {
        "CAI_WORKBENCH_HOST": "https://your-cai-domain.com",
        "CAI_WORKBENCH_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

2. Restart Claude Desktop

## Common Issues

**Build fails with "No module named 'cmlapi'"**
- CAI workbench domain is not reachable.
- Check network connectivity.

**Claude Desktop shows JSON parse errors**  
- Make sure you built the latest Docker image after fixes
- Use STDIO mode, not HTTP mode for Claude Desktop

**API authentication errors**
- Check your CAI_WORKBENCH_API_KEY is valid
- Verify CAI_WORKBENCH_HOST includes https:// prefix