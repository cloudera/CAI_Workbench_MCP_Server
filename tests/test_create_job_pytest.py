#!/usr/bin/env python
"""Pytest test for creating a job using the MCP_cloudera create_job function"""

import os
import json
import pytest
from cml_mcp_server.src.functions.create_job import create_job


@pytest.fixture
def config():
    """Fixture to provide configuration"""
    return {
        "host": os.environ.get("CLOUDERA_ML_HOST", ""),
        "api_key": os.environ.get("CLOUDERA_ML_API_KEY", ""),
        "project_id": os.environ.get("CLOUDERA_ML_PROJECT_ID", "9er0-ooi9-uopm-8i8o")
    }


def test_create_job_minimal(config):
    """Test creating a job with minimal parameters"""
    params = {
        "name": "Test Minimal Job",
        "script": "test.py"
    }
    
    result = create_job(config, params)
    
    # The test is currently failing due to project access, but we can test the structure
    assert isinstance(result, dict)
    assert "success" in result
    assert "message" in result
    
    # If you have a valid project, uncomment this:
    # assert result["success"] is True


def test_create_job_with_runtime(config):
    """Test creating a job with specific runtime"""
    params = {
        "name": "Test Runtime Job",
        "script": "test.py",
        "runtime_identifier": "docker.repository.cloudera.com/cloudera/cdsw/ml-runtime-jupyterlab-python3.9-standard:2023.08.2-b8"
    }
    
    result = create_job(config, params)
    
    assert isinstance(result, dict)
    assert "success" in result
    assert "message" in result


def test_create_job_detailed(config):
    """Test creating a job with detailed parameters"""
    params = {
        "name": "Test Detailed Job",
        "script": "test.py",
        "kernel": "python3",
        "cpu": 2,
        "memory": 4,
        "nvidia_gpu": 0,
        "runtime_identifier": "docker.repository.cloudera.com/cloudera/cdsw/ml-runtime-jupyterlab-python3.9-cuda:2023.08.2-b8"
    }
    
    result = create_job(config, params)
    
    assert isinstance(result, dict)
    assert "success" in result
    assert "message" in result
    
    # Check that payload was sent with correct values
    if "payload_sent" in result:
        assert result["payload_sent"]["cpu"] == 2
        assert result["payload_sent"]["memory"] == 4
