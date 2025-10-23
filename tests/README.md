# CAI Workbench MCP Server Test Suite

Comprehensive test suite for all CAI Workbench MCP Server functions, suitable for CI/CD pipelines.

## Test Files

### `test_all_functions.py` - Comprehensive Unit Test Suite ⭐

**Main test suite covering all 47+ functions in the repository** - CI/CD Ready

### `test_cai_mcp_client.py` - FastMCP Integration Test Suite ⭐

**End-to-end integration tests using FastMCP client** - Tests actual MCP protocol

This test file uses the FastMCP client with in-memory transport to test the actual MCP server:

#### Integration Test Categories:

1. **Server Basics**
   - `test_server_basics`: Tests connectivity and tool discovery (47 tools)

2. **System Tools**
   - `test_system_tools`: Tests get_runtimes_tool (works without credentials)

3. **Project Tools**
   - `test_project_tools`: Tests list_projects_tool, get_project_id_tool

4. **Job Tools**
   - `test_job_tools`: Tests create_job_tool, list_jobs_tool

5. **File Tools**
   - `test_file_tools`: Tests upload_file_tool, list_project_files_tool

6. **Model Tools**
   - `test_model_tools`: Tests create_model_build_tool

7. **Experiment Tools**
   - `test_experiment_tools`: Tests create_experiment_tool

---

### Unit Test Details (test_all_functions.py)

This test file provides complete coverage for all tools/functions with:

#### Test Categories:

1. **Security Tests**
   - `test_no_subprocess_vulnerabilities`: Ensures no API keys are exposed via subprocess
   - `test_functions_follow_security_best_practices`: Validates secure coding practices

2. **Function Signature Tests**
   - `test_all_functions_have_correct_signature`: Verifies all functions accept (config, params)
   - `test_all_modules_import_successfully`: Ensures all modules can be imported

3. **Response Structure Tests**
   - `test_all_functions_return_dict_with_status`: Validates consistent response format
   - `test_all_functions_handle_errors_gracefully`: Ensures proper error handling

4. **Functional Tests**
   - `test_get_runtimes_structure`: Tests runtime retrieval
   - `test_create_job_with_parameters`: Tests job creation with various parameters
   - `test_get_project_id_list_all`: Tests project discovery
   - `test_delete_operations_require_ids`: Tests delete operations
   - `test_list_operations_return_consistent_structure`: Tests list operations

## Running Tests

### Option 1: Unit Tests (test_all_functions.py)
```bash
# Run comprehensive unit tests
uv run pytest tests/test_all_functions.py -v

# Run all pytest tests
uv run pytest tests/ -v
```

### Option 2: FastMCP Integration Tests (test_cai_mcp_client.py)
```bash
# Run full integration test suite
uv run python tests/test_cai_mcp_client.py

# Run quick smoke test (faster)
uv run python tests/test_cai_mcp_client.py --quick
```

### Quick Test
```bash
# Run just security tests
uv run pytest tests/test_all_functions.py::test_no_subprocess_vulnerabilities -v

# Run specific test
uv run pytest tests/test_all_functions.py::test_create_job_with_parameters -v
```

### CI/CD Integration
```bash
# Run with coverage (add pytest-cov to dev dependencies)
uv run pytest tests/ --cov=cai_workbench_mcp_server --cov-report=term-missing

# Run with JUnit XML output for CI systems
uv run pytest tests/ --junit-xml=test-results.xml
```

## Test Coverage

### Functions Tested (47+ total):

**Create Operations:**
- create_application, create_experiment, create_experiment_run, create_job
- create_job_run, create_model_build, create_model_deployment

**Delete Operations:**
- delete_all_jobs, delete_application, delete_experiment, delete_experiment_run
- delete_experiment_run_batch, delete_job, delete_model, delete_project_file

**Get Operations:**
- get_application, get_experiment, get_experiment_run, get_job, get_job_run
- get_model, get_model_build, get_model_deployment, get_project_id, get_runtimes

**List Operations:**
- batch_list_projects, list_applications, list_experiments, list_job_runs
- list_jobs, list_model_builds, list_model_deployments, list_models, list_project_files

**Update Operations:**
- log_experiment_run_batch, restart_application, stop_application, stop_job_run
- stop_model_deployment, update_application, update_experiment, update_experiment_run
- update_job, update_project, update_project_file_metadata

**Upload Operations:**
- upload_file, upload_folder

## Expected Results

### Without Credentials
Most functions will return error responses like:
```json
{
    "success": false,
    "message": "API request error: ...",
    "data": null
}
```

This is **expected** and validates that:
1. Functions handle errors gracefully
2. No crashes occur with invalid/test data
3. Response structure is consistent
4. Security vulnerabilities are absent

### With Valid Credentials
Set these environment variables for full functional testing:
```bash
export CAI_WORKBENCH_HOST="https://your-cai-instance.cloudera.site"
export CAI_WORKBENCH_API_KEY="your-api-key"
export CAI_WORKBENCH_PROJECT_ID="your-project-id"
```

## Test Requirements

### Dependencies
All test dependencies are included in `pyproject.toml`:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
]
```

### Python Version
- Requires Python >= 3.10
- Tests run in Python 3.10, 3.11, 3.12, 3.13

## Security Focus

### Critical Security Tests
1. **No subprocess vulnerabilities**: Ensures API keys are NEVER exposed in process lists
2. **Secure headers**: Validates Authorization headers are used (not URL parameters)
3. **Timeout handling**: Ensures all requests have timeouts to prevent hanging
4. **Error handling**: Validates proper exception handling for all edge cases

### Security Best Practices Enforced
- ✅ Use `requests` library instead of `subprocess.run` for API calls
- ✅ Pass API keys in headers, never in command-line arguments
- ✅ Always specify timeout parameters for HTTP requests
- ✅ Handle all exceptions gracefully with proper error messages

## Continuous Integration

### GitHub Actions Example
```yaml
name: Test Suite
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      - name: Run tests
        run: uv run pytest tests/ -v
```

## Troubleshooting

### Common Issues

**Issue: Tests fail with "NameError: name 'subprocess' is not defined"**
- **Cause**: File still has old subprocess code
- **Fix**: File needs to be updated to use `requests` library

**Issue: Tests are slow**
- **Cause**: Network timeouts
- **Fix**: Tests use mock config, no real network calls should occur

**Issue: Import errors**
- **Cause**: Missing dependencies
- **Fix**: Run `uv sync` to install all dependencies

## Contributing

When adding new functions:
1. Add the function to the `all_functions` fixture in `test_all_functions.py`
2. Ensure it follows the (config, params) signature
3. Ensure it returns dict with success/status and message fields
4. Run tests to verify: `uv run pytest tests/ -v`
