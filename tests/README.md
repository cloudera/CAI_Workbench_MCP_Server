# CML MCP Server Tests

Simple tests using FastMCP client with in-memory transport.

## Running Tests

### Full Test Suite
```bash
# Run all tests
uv run tests/test_cml_mcp_client.py

# Or from project root
uv run python tests/test_cml_mcp_client.py
```

### Quick Smoke Test
```bash
# Just verify server is working
uv run tests/test_cml_mcp_client.py --quick
```

## What Gets Tested

The test suite covers representative tools from each category:

- **Server Basics**: Connectivity and tool discovery (47 tools)
- **System Tools**: `get_runtimes_tool` (works without credentials)
- **Project Tools**: `list_projects_tool`, `get_project_id_tool`
- **Job Tools**: `create_job_tool`, `list_jobs_tool`
- **File Tools**: `upload_file_tool`, `list_project_files_tool`
- **Model Tools**: `create_model_build_tool`
- **Experiment Tools**: `create_experiment_tool`

## Expected Results

Most tools will fail with "Missing required configuration" if you don't have:
- `CLOUDERA_ML_HOST`
- `CLOUDERA_ML_API_KEY`
- `CLOUDERA_ML_PROJECT_ID`

This is expected behavior. The tests verify:
1. The server starts correctly
2. All 47 tools are registered
3. Tools can be called and return proper error messages
4. Tools that don't need credentials (like `get_runtimes_tool`) work correctly


