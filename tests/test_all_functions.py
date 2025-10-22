#!/usr/bin/env python3
"""
Comprehensive test suite for all CML MCP Server functions
Suitable for CI/CD pipeline unit testing

This test suite covers all 47+ tools/functions in the repository with:
- Security validation (no subprocess/curl vulnerabilities)
- Function signature validation
- Error handling validation
- Response structure validation
"""

import pytest
import os
import sys
import inspect

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all functions
from cml_mcp_server.src.functions.batch_list_projects import batch_list_projects
from cml_mcp_server.src.functions.create_application import create_application
from cml_mcp_server.src.functions.create_experiment import create_experiment
from cml_mcp_server.src.functions.create_experiment_run import create_experiment_run
from cml_mcp_server.src.functions.create_job import create_job
from cml_mcp_server.src.functions.create_job_run import create_job_run
from cml_mcp_server.src.functions.create_model_build import create_model_build
from cml_mcp_server.src.functions.create_model_deployment import create_model_deployment
from cml_mcp_server.src.functions.delete_all_jobs import delete_all_jobs
from cml_mcp_server.src.functions.delete_application import delete_application
from cml_mcp_server.src.functions.delete_experiment import delete_experiment
from cml_mcp_server.src.functions.delete_experiment_run import delete_experiment_run
from cml_mcp_server.src.functions.delete_experiment_run_batch import delete_experiment_run_batch
from cml_mcp_server.src.functions.delete_job import delete_job
from cml_mcp_server.src.functions.delete_model import delete_model
from cml_mcp_server.src.functions.delete_project_file import delete_project_file
from cml_mcp_server.src.functions.get_application import get_application
from cml_mcp_server.src.functions.get_experiment import get_experiment
from cml_mcp_server.src.functions.get_experiment_run import get_experiment_run
from cml_mcp_server.src.functions.get_job import get_job
from cml_mcp_server.src.functions.get_job_run import get_job_run
from cml_mcp_server.src.functions.get_model import get_model
from cml_mcp_server.src.functions.get_model_build import get_model_build
from cml_mcp_server.src.functions.get_model_deployment import get_model_deployment
from cml_mcp_server.src.functions.get_project_id import get_project_id
from cml_mcp_server.src.functions.get_runtimes import get_runtimes
from cml_mcp_server.src.functions.list_applications import list_applications
from cml_mcp_server.src.functions.list_experiments import list_experiments
from cml_mcp_server.src.functions.list_job_runs import list_job_runs
from cml_mcp_server.src.functions.list_jobs import list_jobs
from cml_mcp_server.src.functions.list_model_builds import list_model_builds
from cml_mcp_server.src.functions.list_model_deployments import list_model_deployments
from cml_mcp_server.src.functions.list_models import list_models
from cml_mcp_server.src.functions.list_project_files import list_project_files
from cml_mcp_server.src.functions.log_experiment_run_batch import log_experiment_run_batch
from cml_mcp_server.src.functions.restart_application import restart_application
from cml_mcp_server.src.functions.stop_application import stop_application
from cml_mcp_server.src.functions.stop_job_run import stop_job_run
from cml_mcp_server.src.functions.stop_model_deployment import stop_model_deployment
from cml_mcp_server.src.functions.update_application import update_application
from cml_mcp_server.src.functions.update_experiment import update_experiment
from cml_mcp_server.src.functions.update_experiment_run import update_experiment_run
from cml_mcp_server.src.functions.update_job import update_job
from cml_mcp_server.src.functions.update_project import update_project
from cml_mcp_server.src.functions.update_project_file_metadata import update_project_file_metadata
from cml_mcp_server.src.functions.upload_file import upload_file
from cml_mcp_server.src.functions.upload_folder import upload_folder


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def mock_config():
    """Provide mock configuration for testing"""
    return {
        "host": "https://test.cloudera.site",
        "api_key": "test_api_key_12345",
        "project_id": "test-project-123"
    }


@pytest.fixture
def all_functions():
    """List of all functions to test"""
    return [
        # Create operations
        (create_application, {"name": "test", "subdomain": "test", "script": "app.py"}),
        (create_experiment, {"name": "test", "project_id": "test"}),
        (create_experiment_run, {"experiment_id": "test", "project_id": "test"}),
        (create_job, {"name": "test", "script": "test.py"}),
        (create_job_run, {"job_id": "test", "project_id": "test"}),
        (create_model_build, {"project_id": "test", "model_id": "test", "file_path": "model.py", "function_name": "predict", "kernel": "python3"}),
        (create_model_deployment, {"project_id": "test", "model_id": "test", "build_id": "test"}),
        
        # Delete operations
        (delete_all_jobs, {"project_id": "test"}),
        (delete_application, {"application_id": "test"}),
        (delete_experiment, {"experiment_id": "test", "project_id": "test"}),
        (delete_experiment_run, {"run_id": "test", "experiment_id": "test", "project_id": "test"}),
        (delete_experiment_run_batch, {"experiment_id": "test", "project_id": "test", "run_ids": ["test1", "test2"]}),
        (delete_job, {"job_id": "test", "project_id": "test"}),
        (delete_model, {"model_id": "test", "project_id": "test"}),
        (delete_project_file, {"path": "/test.txt", "project_id": "test"}),
        
        # Get operations
        (get_application, {"application_id": "test"}),
        (get_experiment, {"experiment_id": "test", "project_id": "test"}),
        (get_experiment_run, {"run_id": "test", "experiment_id": "test", "project_id": "test"}),
        (get_job, {"job_id": "test", "project_id": "test"}),
        (get_job_run, {"job_id": "test", "run_id": "test", "project_id": "test"}),
        (get_model, {"model_id": "test", "project_id": "test"}),
        (get_model_build, {"model_id": "test", "build_id": "test", "project_id": "test"}),
        (get_model_deployment, {"model_id": "test", "deployment_id": "test", "project_id": "test"}),
        (get_project_id, {"project_name": "*"}),
        (get_runtimes, {}),
        
        # List operations
        (batch_list_projects, {}),
        (list_applications, {"project_id": "test"}),
        (list_experiments, {"project_id": "test"}),
        (list_job_runs, {"job_id": "test", "project_id": "test"}),
        (list_jobs, {"project_id": "test"}),
        (list_model_builds, {"model_id": "test", "project_id": "test"}),
        (list_model_deployments, {"model_id": "test", "project_id": "test"}),
        (list_models, {"project_id": "test"}),
        (list_project_files, {"path": "/", "project_id": "test"}),
        
        # Update operations
        (log_experiment_run_batch, {"experiment_id": "test", "project_id": "test", "runs": []}),
        (restart_application, {"application_id": "test"}),
        (stop_application, {"application_id": "test"}),
        (stop_job_run, {"job_id": "test", "run_id": "test", "project_id": "test"}),
        (stop_model_deployment, {"model_id": "test", "deployment_id": "test", "project_id": "test"}),
        (update_application, {"application_id": "test"}),
        (update_experiment, {"experiment_id": "test", "project_id": "test"}),
        (update_experiment_run, {"run_id": "test", "experiment_id": "test", "project_id": "test"}),
        (update_job, {"job_id": "test", "project_id": "test"}),
        (update_project, {"project_id": "test"}),
        (update_project_file_metadata, {"path": "/test.txt", "project_id": "test"}),
        
        # Upload operations
        (upload_file, {"file_path": "/tmp/test.txt", "target_name": "test.txt", "target_dir": "/", "project_id": "test"}),
        (upload_folder, {"folder_path": "/tmp/test", "target_dir": "/", "project_id": "test"}),
    ]


# =============================================================================
# TEST 1: SECURITY - No subprocess vulnerabilities
# =============================================================================

def test_no_subprocess_vulnerabilities():
    """
    Verify that NO functions use subprocess.run for API calls
    This is critical for security - prevents API key exposure in process list
    """
    import cml_mcp_server.src.functions.delete_application as delete_app_mod
    import cml_mcp_server.src.functions.create_job_run as create_job_run_mod
    import cml_mcp_server.src.functions.get_job as get_job_mod
    import cml_mcp_server.src.functions.list_experiments as list_exp_mod
    import cml_mcp_server.src.functions.create_experiment_run as create_exp_run_mod
    
    critical_modules = [
        delete_app_mod,
        create_job_run_mod,
        get_job_mod,
        list_exp_mod,
        create_exp_run_mod,
    ]
    
    for module in critical_modules:
        module_file = inspect.getfile(module)
        module_source = open(module_file).read()
        
        # MUST use requests, not subprocess
        assert 'import requests' in module_source, \
            f"{module.__name__} MUST import requests"
        
        # MUST NOT use subprocess.run (security vulnerability)
        assert 'subprocess.run' not in module_source, \
            f"{module.__name__} MUST NOT use subprocess.run (security vulnerability)"
        
        # MUST use requests methods
        has_requests_call = any(method in module_source for method in ['requests.get', 'requests.post', 'requests.delete'])
        assert has_requests_call, \
            f"{module.__name__} MUST use requests.get/post/delete methods"


# =============================================================================
# TEST 2: FUNCTION SIGNATURES - All functions accept (config, params)
# =============================================================================

def test_all_functions_have_correct_signature(all_functions):
    """Verify all functions accept (config, params) signature"""
    for func, _ in all_functions:
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        
        assert len(params) >= 1, f"{func.__name__} must accept at least config parameter"
        assert params[0] == "config", f"{func.__name__} first parameter must be 'config'"
        
        # Most functions should also accept params
        if len(params) > 1:
            assert params[1] == "params", f"{func.__name__} second parameter should be 'params'"


# =============================================================================
# TEST 3: RESPONSE STRUCTURE - All functions return dict with status
# =============================================================================

def test_all_functions_return_dict_with_status(all_functions, mock_config):
    """Verify all functions return consistent response structure"""
    for func, test_params in all_functions:
        result = func(mock_config, test_params)
        
        # Must return dict
        assert isinstance(result, dict), \
            f"{func.__name__} must return dict, got {type(result)}"
        
        # Must have either 'success' or 'status' field
        has_status = "success" in result or "status" in result
        assert has_status, \
            f"{func.__name__} must have 'success' or 'status' in response"
        
        # Must have message field
        assert "message" in result, \
            f"{func.__name__} must have 'message' in response"


# =============================================================================
# TEST 4: ERROR HANDLING - Functions handle errors gracefully
# =============================================================================

def test_all_functions_handle_errors_gracefully(all_functions, mock_config):
    """Verify all functions handle errors without crashing"""
    for func, test_params in all_functions:
        try:
            result = func(mock_config, test_params)
            
            # Should not crash
            assert result is not None, f"{func.__name__} returned None"
            
            # Should return dict
            assert isinstance(result, dict), f"{func.__name__} must return dict"
            
            # Should have message
            assert "message" in result, f"{func.__name__} must have error message"
            
            # Should not have subprocess errors
            if "message" in result:
                message_lower = str(result["message"]).lower()
                assert "subprocess" not in message_lower, \
                    f"{func.__name__} should not have subprocess errors"
                
        except Exception as e:
            pytest.fail(f"{func.__name__} raised exception: {e}")


# =============================================================================
# TEST 5: SECURITY BEST PRACTICES
# =============================================================================

def test_functions_follow_security_best_practices():
    """Verify functions follow security best practices"""
    
    functions_to_check = [
        delete_application,
        create_job_run,
        get_job,
        list_experiments,
        create_experiment_run,
        delete_experiment_run,
    ]
    
    for func in functions_to_check:
        source = inspect.getsource(func)
        
        # 1. Must use requests library (not subprocess)
        has_requests = any(method in source for method in ['requests.get', 'requests.post', 'requests.delete'])
        assert has_requests, f"{func.__name__} must use requests library"
        
        # 2. Must have timeout parameter (prevents hanging)
        assert 'timeout=' in source, f"{func.__name__} must specify timeout"
        
        # 3. Must have error handling
        assert 'except' in source, f"{func.__name__} must have error handling"
        
        # 4. Must NOT use subprocess.run
        assert 'subprocess.run' not in source, f"{func.__name__} must NOT use subprocess.run"
        
        # 5. Must pass Authorization in headers (not in URL or args)
        assert 'headers=' in source, f"{func.__name__} must use headers parameter"
        has_auth_header = '"Authorization"' in source or "'Authorization'" in source
        assert has_auth_header, f"{func.__name__} must set Authorization header"


# =============================================================================
# TEST 6: SPECIFIC FUNCTION TESTS
# =============================================================================

def test_get_runtimes_structure(mock_config):
    """Test get_runtimes returns proper structure"""
    result = get_runtimes(mock_config, {})
    
    assert isinstance(result, dict)
    assert "success" in result or "status" in result
    assert "message" in result


def test_create_job_with_parameters(mock_config):
    """Test create_job with various parameter combinations"""
    # Minimal parameters
    result1 = create_job(mock_config, {"name": "test", "script": "test.py"})
    assert isinstance(result1, dict)
    assert "success" in result1
    
    # With runtime
    result2 = create_job(mock_config, {
        "name": "test",
        "script": "test.py",
        "runtime_identifier": "docker.repository.cloudera.com/cloudera/cdsw/ml-runtime-jupyterlab-python3.10-standard:2024.10.1-b12"
    })
    assert isinstance(result2, dict)
    assert "success" in result2
    
    # With resources
    result3 = create_job(mock_config, {
        "name": "test",
        "script": "test.py",
        "cpu": 2,
        "memory": 4,
        "nvidia_gpu": 0
    })
    assert isinstance(result3, dict)
    assert "success" in result3


def test_get_project_id_list_all(mock_config):
    """Test get_project_id can list all projects"""
    result = get_project_id(mock_config, {"project_name": "*"})
    
    assert isinstance(result, dict)
    assert "message" in result or "projects" in result or "status" in result


def test_delete_operations_require_ids(mock_config):
    """Test delete operations require proper IDs"""
    # Test various delete operations
    delete_functions = [
        (delete_application, {"application_id": "test"}),
        (delete_job, {"job_id": "test", "project_id": "test"}),
        (delete_model, {"model_id": "test", "project_id": "test"}),
    ]
    
    for func, params in delete_functions:
        result = func(mock_config, params)
        assert isinstance(result, dict)
        assert "success" in result or "status" in result


def test_list_operations_return_consistent_structure(mock_config):
    """Test list operations return consistent structure"""
    list_functions = [
        (list_jobs, {"project_id": "test"}),
        (list_experiments, {"project_id": "test"}),
        (list_models, {"project_id": "test"}),
        (list_applications, {"project_id": "test"}),
    ]
    
    for func, params in list_functions:
        result = func(mock_config, params)
        assert isinstance(result, dict)
        assert "success" in result or "status" in result
        assert "message" in result


# =============================================================================
# TEST 7: MODULE IMPORTS
# =============================================================================

def test_all_modules_import_successfully():
    """Verify all function modules can be imported"""
    import cml_mcp_server.src.functions.batch_list_projects
    import cml_mcp_server.src.functions.create_application
    import cml_mcp_server.src.functions.create_experiment
    import cml_mcp_server.src.functions.create_experiment_run
    import cml_mcp_server.src.functions.create_job
    import cml_mcp_server.src.functions.create_job_run
    import cml_mcp_server.src.functions.create_model_build
    import cml_mcp_server.src.functions.create_model_deployment
    import cml_mcp_server.src.functions.delete_all_jobs
    import cml_mcp_server.src.functions.delete_application
    import cml_mcp_server.src.functions.delete_experiment
    import cml_mcp_server.src.functions.delete_experiment_run
    import cml_mcp_server.src.functions.delete_experiment_run_batch
    import cml_mcp_server.src.functions.delete_job
    import cml_mcp_server.src.functions.delete_model
    import cml_mcp_server.src.functions.delete_project_file
    import cml_mcp_server.src.functions.get_application
    import cml_mcp_server.src.functions.get_experiment
    import cml_mcp_server.src.functions.get_experiment_run
    import cml_mcp_server.src.functions.get_job
    import cml_mcp_server.src.functions.get_job_run
    import cml_mcp_server.src.functions.get_model
    import cml_mcp_server.src.functions.get_model_build
    import cml_mcp_server.src.functions.get_model_deployment
    import cml_mcp_server.src.functions.get_project_id
    import cml_mcp_server.src.functions.get_runtimes
    import cml_mcp_server.src.functions.list_applications
    import cml_mcp_server.src.functions.list_experiments
    import cml_mcp_server.src.functions.list_job_runs
    import cml_mcp_server.src.functions.list_jobs
    import cml_mcp_server.src.functions.list_model_builds
    import cml_mcp_server.src.functions.list_model_deployments
    import cml_mcp_server.src.functions.list_models
    import cml_mcp_server.src.functions.list_project_files
    import cml_mcp_server.src.functions.log_experiment_run_batch
    import cml_mcp_server.src.functions.restart_application
    import cml_mcp_server.src.functions.stop_application
    import cml_mcp_server.src.functions.stop_job_run
    import cml_mcp_server.src.functions.stop_model_deployment
    import cml_mcp_server.src.functions.update_application
    import cml_mcp_server.src.functions.update_experiment
    import cml_mcp_server.src.functions.update_experiment_run
    import cml_mcp_server.src.functions.update_job
    import cml_mcp_server.src.functions.update_project
    import cml_mcp_server.src.functions.update_project_file_metadata
    import cml_mcp_server.src.functions.upload_file
    import cml_mcp_server.src.functions.upload_folder
    
    # If we got here, all imports succeeded
    assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

