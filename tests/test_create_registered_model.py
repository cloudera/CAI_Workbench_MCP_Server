"""Unit tests for create_registered_model (tags JSON string handling)."""

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
    """MCP passes tags as a string; API expects a JSON array — verify payload."""
    captured = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["url"] = url
        captured["json"] = json
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json = MagicMock(return_value={"model_id": "mid", "name": "m"})
        return resp

    params = {
        "project_id": "p1",
        "experiment_id": "e1",
        "run_id": "r1",
        "model_path": "model",
        "model_name": "test-model",
        "tags": '[{"key": "env", "value": "ci"}]',
    }

    with patch("cai_workbench_mcp_server.src.functions.create_registered_model.requests.post", fake_post):
        result = create_registered_model(config, params)

    assert result["success"] is True
    assert captured["json"]["tags"] == [{"key": "env", "value": "ci"}]
    assert captured["url"].endswith("/api/v2/registry/models")


def test_create_registered_model_invalid_tags_string_returns_error(config):
    params = {
        "project_id": "p1",
        "experiment_id": "e1",
        "run_id": "r1",
        "model_path": "model",
        "model_name": "test-model",
        "tags": "not-json",
    }

    result = create_registered_model(config, params)

    assert result["success"] is False
    assert "tags must be a JSON array string" in result["message"]


def test_create_registered_model_accepts_list_tags(config):
    """Non-string tags are forwarded as-is (callers passing native lists)."""
    captured = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["json"] = json
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json = MagicMock(return_value={})
        return resp

    tags = [{"key": "a", "value": "b"}]
    params = {
        "project_id": "p1",
        "experiment_id": "e1",
        "run_id": "r1",
        "model_path": "model",
        "model_name": "test-model",
        "tags": tags,
    }

    with patch("cai_workbench_mcp_server.src.functions.create_registered_model.requests.post", fake_post):
        result = create_registered_model(config, params)

    assert result["success"] is True
    assert captured["json"]["tags"] == tags
