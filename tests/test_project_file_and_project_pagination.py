from unittest.mock import MagicMock, patch

from cai_workbench_mcp_server.src.functions.delete_project_file import delete_project_file
from cai_workbench_mcp_server.src.functions.get_project_id import get_project_id
from cai_workbench_mcp_server.src.functions.list_project_files import list_project_files


def test_get_project_id_paginates_all_projects():
    config = {"host": "https://ml.example", "api_key": "token"}
    calls = []

    def fake_get(url, headers=None, params=None, timeout=None):
        calls.append(params)
        response = MagicMock()
        response.raise_for_status = MagicMock()
        if len(calls) == 1:
            response.json = MagicMock(
                return_value={
                    "projects": [{"name": "first", "id": "p1"}],
                    "next_page_token": "next",
                }
            )
        else:
            response.json = MagicMock(return_value={"projects": [{"name": "target", "id": "p2"}]})
        return response

    with patch("cai_workbench_mcp_server.src.functions.get_project_id.requests.get", fake_get):
        result = get_project_id(config, {"project_name": "target"})

    assert result["status"] == "success"
    assert result["project_id"] == "p2"
    assert calls == [{"page_size": 200}, {"page_size": 200, "page_token": "next"}]


def test_list_project_files_uses_url_segment_for_subdirectory():
    config = {"host": "https://ml.example", "api_key": "token"}
    captured = {}

    def fake_get(url, headers=None, timeout=None):
        captured["url"] = url
        response = MagicMock(status_code=200)
        response.json = MagicMock(return_value={"files": []})
        return response

    with patch("cai_workbench_mcp_server.src.functions.list_project_files.requests.get", fake_get):
        result = list_project_files(config, {"project_id": "p1", "path": "/dir with spaces/app.py"})

    assert result["success"] is True
    assert captured["url"].endswith("/api/v2/projects/p1/files/dir%20with%20spaces/app.py")


def test_delete_project_file_refuses_root_and_parent_segments():
    config = {"host": "https://ml.example", "api_key": "token", "project_id": "p1"}

    assert delete_project_file(config, {"file_path": "/"})["success"] is False
    assert delete_project_file(config, {"file_path": "dir/../secret"})["success"] is False


def test_delete_project_file_uses_url_segment():
    config = {"host": "https://ml.example", "api_key": "token", "project_id": "p1"}
    captured = {}

    def fake_delete(url, headers=None, timeout=None):
        captured["url"] = url
        response = MagicMock(status_code=204)
        response.text = ""
        return response

    with patch("cai_workbench_mcp_server.src.functions.delete_project_file.requests.delete", fake_delete):
        result = delete_project_file(config, {"file_path": "/dir with spaces/app.py"})

    assert result["success"] is True
    assert captured["url"].endswith("/api/v2/projects/p1/files/dir%20with%20spaces/app.py")
