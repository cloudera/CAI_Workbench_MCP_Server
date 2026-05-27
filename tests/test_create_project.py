"""Unit tests for create_project defaults."""

from unittest.mock import MagicMock, patch

from cai_workbench_mcp_server.src.functions.create_project import (
    DEFAULT_ENGINE_TYPE,
    DEFAULT_TEMPLATE,
    create_project,
)


def _config():
    return {"host": "https://ml-example.cloudera.site", "api_key": "test-key"}


@patch("cai_workbench_mcp_server.src.functions.create_project.setup_client")
def test_create_project_defaults_template_and_engine_type(mock_setup_client):
    mock_client = MagicMock()
    mock_setup_client.return_value = mock_client
    mock_client.create_project.return_value = MagicMock(
        to_dict=lambda: {"id": "proj-1", "name": "demo"}
    )

    result = create_project(_config(), {"name": "demo"})

    assert result["success"] is True
    mock_client.create_project.assert_called_once_with(
        {
            "name": "demo",
            "template": DEFAULT_TEMPLATE,
            "default_project_engine_type": DEFAULT_ENGINE_TYPE,
        }
    )


@patch("cai_workbench_mcp_server.src.functions.create_project.setup_client")
def test_create_project_honors_explicit_overrides(mock_setup_client):
    mock_client = MagicMock()
    mock_setup_client.return_value = mock_client
    mock_client.create_project.return_value = MagicMock(to_dict=lambda: {"id": "proj-2"})

    create_project(
        _config(),
        {
            "name": "demo",
            "template": "Python",
            "default_project_engine_type": "legacy_engine",
            "description": "test project",
        },
    )

    mock_client.create_project.assert_called_once_with(
        {
            "name": "demo",
            "template": "Python",
            "default_project_engine_type": "legacy_engine",
            "description": "test project",
        }
    )


def test_create_project_requires_name():
    result = create_project(_config(), {})
    assert result["success"] is False
    assert "name is required" in result["message"]


@patch("cai_workbench_mcp_server.src.functions.create_project.setup_client")
def test_create_project_includes_team_name_from_param(mock_setup_client):
    mock_client = MagicMock()
    mock_setup_client.return_value = mock_client
    mock_client.create_project.return_value = MagicMock(to_dict=lambda: {"id": "proj-3"})

    create_project(_config(), {"name": "demo", "team_name": "Team1"})

    mock_client.create_project.assert_called_once_with(
        {
            "name": "demo",
            "template": DEFAULT_TEMPLATE,
            "default_project_engine_type": DEFAULT_ENGINE_TYPE,
            "team_name": "Team1",
        }
    )


@patch("cai_workbench_mcp_server.src.functions.create_project.setup_client")
def test_create_project_team_name_from_config(mock_setup_client):
    mock_client = MagicMock()
    mock_setup_client.return_value = mock_client
    mock_client.create_project.return_value = MagicMock(to_dict=lambda: {"id": "proj-4"})

    config = _config()
    config["team"] = "Team1"
    create_project(config, {"name": "demo"})

    body = mock_client.create_project.call_args[0][0]
    assert body["team_name"] == "Team1"


@patch("cai_workbench_mcp_server.src.functions.create_project.setup_client")
def test_create_project_param_team_name_overrides_config(mock_setup_client):
    mock_client = MagicMock()
    mock_setup_client.return_value = mock_client
    mock_client.create_project.return_value = MagicMock(to_dict=lambda: {"id": "proj-5"})

    config = _config()
    config["team"] = "Team1"
    create_project(config, {"name": "demo", "team_name": "Team2"})

    body = mock_client.create_project.call_args[0][0]
    assert body["team_name"] == "Team2"
