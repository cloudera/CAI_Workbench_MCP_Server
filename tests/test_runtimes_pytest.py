#!/usr/bin/env python
"""Pytest test for getting available runtimes"""

import os
import pytest
from cml_mcp_server.src.functions.get_runtimes import get_runtimes


@pytest.fixture
def config():
    """Fixture to provide configuration"""
    return {
        "host": os.environ.get("CLOUDERA_ML_HOST", ""),
        "api_key": os.environ.get("CLOUDERA_ML_API_KEY", "")
    }


def test_get_runtimes(config):
    """Test retrieving available runtimes"""
    result = get_runtimes(config, {})
    
    # Check result structure
    assert isinstance(result, dict)
    assert "success" in result
    assert "message" in result
    
    # If successful, check runtimes
    if result.get("success"):
        assert "runtimes" in result
        assert isinstance(result["runtimes"], list)
        assert len(result["runtimes"]) > 0
        
        # Check first runtime structure
        first_runtime = result["runtimes"][0]
        assert "identifier" in first_runtime
        assert "edition" in first_runtime
        
        # Print summary for debugging
        print(f"\nFound {len(result['runtimes'])} runtimes")
        
        # Group by edition
        editions = {}
        for runtime in result["runtimes"]:
            edition = runtime.get("edition", "Unknown")
            editions[edition] = editions.get(edition, 0) + 1
        
        print("Runtimes by edition:")
        for edition, count in editions.items():
            print(f"  - {edition}: {count}")


def test_runtime_identifiers_format(config):
    """Test that runtime identifiers follow expected format"""
    result = get_runtimes(config, {})
    
    if result.get("success") and result.get("runtimes"):
        for runtime in result["runtimes"]:
            identifier = runtime.get("identifier", "")
            
            # Check identifier format (should contain docker.repository.cloudera.com)
            assert "docker.repository.cloudera.com" in identifier
            assert identifier.endswith(":2024.10.1-b12") or ":20" in identifier  # Version tag
            
            # Check for Python version in identifier
            assert "python" in identifier.lower() or "conda" in identifier.lower()
