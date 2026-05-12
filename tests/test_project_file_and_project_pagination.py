"""Unit tests for project file and pagination functions (cmlapi-backed)."""

from unittest.mock import MagicMock, patch, call

from cai_workbench_mcp_server.src.functions.delete_project_file import delete_project_file
from cai_workbench_mcp_server.src.functions.get_project_id import get_project_id
from cai_workbench_mcp_server.src.functions.list_project_files import list_project_files


def test_get_project_id_paginates_all_projects():
    config = {"host": "https://ml.example", "api_key": "token"}

    mock_client = MagicMock()
    # First page returns one project + next_page_token
    page1 = MagicMock()
    page1.to_dict.return_value = {
        "projects": [{"name": "first", "id": "p1"}],
        "next_page_token": "next",
    }
    # Second page returns target project, no next token
    page2 = MagicMock()
    page2.to_dict.return_value = {
        "projects": [{"name": "target", "id": "p2"}],
        "next_page_token": None,
    }
    mock_client.list_projects.side_effect = [page1, page2]

    with patch("cai_workbench_mcp_server.src.functions.get_project_id.setup_client", return_value=mock_client):
        result = get_project_id(config, {"project_name": "target"})

    assert result["status"] == "success"
    assert result["project_id"] == "p2"
    assert mock_client.list_projects.call_count == 2


def test_get_project_id_list_all_reports_pagination_metadata():
    config = {"host": "https://ml.example", "api_key": "token"}

    mock_client = MagicMock()
    page = MagicMock()
    page.to_dict.return_value = {
        "projects": [{"name": "first", "id": "p1"}],
        "next_page_token": None,
    }
    mock_client.list_projects.return_value = page

    with patch("cai_workbench_mcp_server.src.functions.get_project_id.setup_client", return_value=mock_client):
        result = get_project_id(config, {"project_name": "*"})

    assert result["status"] == "success"
    assert result["count"] == 1


def test_list_project_files_uses_cmlapi():
    config = {"host": "https://ml.example", "api_key": "token"}

    mock_client = MagicMock()
    mock_result = MagicMock()
    mock_result.to_dict.return_value = {"files": []}
    mock_client.list_project_files.return_value = mock_result

    with patch("cai_workbench_mcp_server.src.functions.list_project_files.setup_client", return_value=mock_client):
        result = list_project_files(config, {"project_id": "p1", "path": "/dir with spaces/app.py"})

    assert result["success"] is True
    mock_client.list_project_files.assert_called_once_with("p1", "/dir with spaces/app.py")


def test_delete_project_file_calls_cmlapi():
    config = {"host": "https://ml.example", "api_key": "token", "project_id": "p1"}

    mock_client = MagicMock()
    mock_result = MagicMock()
    mock_result.to_dict.return_value = {}
    mock_client.delete_project_file.return_value = mock_result

    with patch("cai_workbench_mcp_server.src.functions.delete_project_file.setup_client", return_value=mock_client):
        result = delete_project_file(config, {"file_path": "/dir/app.py"})

    assert result["success"] is True
    mock_client.delete_project_file.assert_called_once_with("p1", "/dir/app.py")


def test_delete_project_file_missing_params():
    config = {"host": "https://ml.example", "api_key": "token"}

    result = delete_project_file(config, {})
    assert result["success"] is False
