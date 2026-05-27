"""Unit tests for list_teams."""

from unittest.mock import MagicMock, patch

from cmlapi.rest import ApiException

from cai_workbench_mcp_server.src.functions.list_teams import list_teams


def _config():
    return {"host": "https://ml-example.cloudera.site", "api_key": "test-key"}


def _quota_response(items, next_page_token=""):
    payload = MagicMock()
    payload.to_dict.return_value = items
    return payload


@patch("cai_workbench_mcp_server.src.functions.list_teams.setup_client")
def test_list_teams_from_accelerator_quota(mock_setup_client):
    mock_client = MagicMock()
    mock_setup_client.return_value = mock_client
    mock_client.list_teams_accelerator_quota.return_value = _quota_response(
        {
            "team_accelerator_quota": [
                {"team_name": "Team1"},
                {"team_name": "Team2"},
            ],
            "next_page_token": "",
        }
    )

    result = list_teams(_config(), {})

    assert result["success"] is True
    assert result["data"]["teams"] == ["Team1", "Team2"]
    assert result["data"]["source"] == "list_teams_accelerator_quota"
    mock_client.list_groups_quota.assert_not_called()


@patch("cai_workbench_mcp_server.src.functions.list_teams.setup_client")
def test_list_teams_falls_back_to_groups_quota(mock_setup_client):
    mock_client = MagicMock()
    mock_setup_client.return_value = mock_client
    mock_client.list_teams_accelerator_quota.side_effect = ApiException(status=403, reason="Forbidden")
    mock_client.list_groups_quota.return_value = _quota_response(
        {
            "group_quota": [
                {"group": {"user_name": "Team1", "name": "Team 1"}},
                {"group": {"user_name": "Team1", "name": "Team 1"}},
                {"group": {"user_name": "Team3", "name": "Team 3"}},
            ],
            "next_page_token": "",
        }
    )

    result = list_teams(_config(), {})

    assert result["success"] is True
    assert result["data"]["teams"] == ["Team1", "Team3"]
    assert result["data"]["source"] == "list_groups_quota"


@patch("cai_workbench_mcp_server.src.functions.list_teams.setup_client")
def test_list_teams_empty_when_no_sources(mock_setup_client):
    mock_client = MagicMock()
    mock_setup_client.return_value = mock_client
    mock_client.list_teams_accelerator_quota.return_value = _quota_response(
        {"team_accelerator_quota": [], "next_page_token": ""}
    )
    mock_client.list_groups_quota.return_value = _quota_response(
        {"group_quota": [], "next_page_token": ""}
    )

    result = list_teams(_config(), {})

    assert result["success"] is False
    assert result["data"]["teams"] == []
    assert "CAI_WORKBENCH_TEAM" in result["message"]
