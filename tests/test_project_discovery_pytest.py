#!/usr/bin/env python
"""Pytest test for finding projects using the get_project_id function"""

import os
import json
import pytest
from cml_mcp_server.src.functions.get_project_id import get_project_id


@pytest.fixture
def config():
    """Fixture to provide configuration"""
    return {
        "host": os.environ.get("CLOUDERA_ML_HOST", ""),
        "api_key": os.environ.get("CLOUDERA_ML_API_KEY", "")
    }


def test_list_all_projects(config):
    """Test listing all available projects"""
    # Using "*" as project_name lists all projects
    params = {"project_name": "*"}
    
    result = get_project_id(config, params)
    
    # Check result structure
    assert isinstance(result, dict)
    assert "success" in result
    assert "message" in result
    
    # If successful, check projects list
    if result.get("success"):
        assert "projects" in result
        assert isinstance(result["projects"], list)
        
        # Print projects for debugging
        print(f"\nFound {len(result['projects'])} projects:")
        for project in result["projects"]:
            print(f"  - {project.get('name')} (ID: {project.get('id')})")


def test_find_specific_project(config):
    """Test finding a specific project by name"""
    # This test assumes you have at least one project
    # First, get all projects
    all_projects = get_project_id(config, {"project_name": "*"})
    
    if all_projects.get("success") and all_projects.get("projects"):
        # Use the first project's name for testing
        first_project = all_projects["projects"][0]
        project_name = first_project.get("name")
        
        # Now search for this specific project
        params = {"project_name": project_name}
        result = get_project_id(config, params)
        
        assert result["success"] is True
        assert "project_id" in result
        assert result["project_id"] == first_project.get("id")
        assert result["message"] == f"Found project '{project_name}'"


def test_project_not_found(config):
    """Test behavior when project doesn't exist"""
    params = {"project_name": "NonExistentProject12345"}
    
    result = get_project_id(config, params)
    
    assert isinstance(result, dict)
    assert result["success"] is False
    assert "not found" in result["message"].lower()


@pytest.mark.parametrize("invalid_name", [
    "",  # Empty string
    " ",  # Just whitespace
    None,  # None value
])
def test_invalid_project_names(config, invalid_name):
    """Test handling of invalid project names"""
    params = {"project_name": invalid_name}
    
    result = get_project_id(config, params)
    
    assert isinstance(result, dict)
    assert "success" in result
    # Should either fail gracefully or handle the invalid input
