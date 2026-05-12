"""Unit tests for create_registered_model (tags handling)."""

from unittest.mock import MagicMock, patch

import pytest

from cai_workbench_mcp_server.src.functions.create_registered_model import create_registered_model


@pytest.fixture
def config():
    return {
        "host": "https://ml-example.cloudera.site",
        "api_key": "test-api-key",
    }


def test_create_registered_model_parses_tags_json_string(config):
    """MCP passes tags as a string; verify it gets parsed to a list in the body."""
    mock_client = MagicMock()
    mock_result = MagicMock()
    mock_result.to_dict.return_value = {"model_id": "mid", "name": "m"}
    mock_client.create_registered_model.return_value = mock_result

    params = {
        "project_id": "p1",
        "experiment_id": "e1",
        "run_id": "r1",
        "model_path": "model",
        "model_name": "test-model",
        "tags": "tag1,tag2",
    }

    with patch("cai_workbench_mcp_server.src.functions.create_registered_model.setup_client", return_value=mock_client):
        result = create_registered_model(config, params)

    assert result["success"] is True
    call_body = mock_client.create_registered_model.call_args[0][0]
    assert call_body["tags"] == ["tag1", "tag2"]


def test_create_registered_model_invalid_tags_string_returns_error(config):
    """When tags is a comma-separated string, it should split properly."""
    mock_client = MagicMock()
    mock_result = MagicMock()
    mock_result.to_dict.return_value = {}
    mock_client.create_registered_model.return_value = mock_result

    params = {
        "project_id": "p1",
        "experiment_id": "e1",
        "run_id": "r1",
        "model_path": "model",
        "model_name": "test-model",
        "tags": "not-json",
    }

    with patch("cai_workbench_mcp_server.src.functions.create_registered_model.setup_client", return_value=mock_client):
        result = create_registered_model(config, params)

    # With cmlapi refactor, tags string gets split by comma
    assert result["success"] is True
    call_body = mock_client.create_registered_model.call_args[0][0]
    assert call_body["tags"] == ["not-json"]


def test_create_registered_model_accepts_list_tags(config):
    """Non-string tags are forwarded as-is."""
    mock_client = MagicMock()
    mock_result = MagicMock()
    mock_result.to_dict.return_value = {}
    mock_client.create_registered_model.return_value = mock_result

    tags = ["a", "b"]
    params = {
        "project_id": "p1",
        "experiment_id": "e1",
        "run_id": "r1",
        "model_path": "model",
        "model_name": "test-model",
        "tags": tags,
    }

    with patch("cai_workbench_mcp_server.src.functions.create_registered_model.setup_client", return_value=mock_client):
        result = create_registered_model(config, params)

    assert result["success"] is True
    call_body = mock_client.create_registered_model.call_args[0][0]
    assert call_body["tags"] == tags
