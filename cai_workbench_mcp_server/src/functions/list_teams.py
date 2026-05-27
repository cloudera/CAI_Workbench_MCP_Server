"""List teams for project creation (team username values for CreateProjectRequest.team_name)."""

from typing import Any, Callable, Dict, List
try:
    from cmlapi.rest import ApiException
except ImportError:
    class ApiException(Exception):
        """Placeholder when cmlapi is not installed."""
        status = None
        body = None
from .http_helpers import setup_client, serialize_result


def _names_from_accelerator_quota(data: Dict[str, Any]) -> List[str]:
    names = []
    for entry in data.get("team_accelerator_quota") or []:
        team_name = entry.get("team_name")
        if team_name:
            names.append(team_name)
    return names


def _names_from_groups_quota(data: Dict[str, Any]) -> List[str]:
    names = []
    for entry in data.get("group_quota") or []:
        group = entry.get("group") or {}
        user_name = group.get("user_name")
        if user_name:
            names.append(user_name)
    return names


def _collect_team_names(client, method_name: str, extract: Callable[[Dict[str, Any]], List[str]], params: Dict[str, Any]) -> List[str]:
    call = getattr(client, method_name)
    names: List[str] = []
    page_token = None
    while True:
        kwargs = {}
        for key in ("search_filter", "page_size", "page_token", "sort"):
            value = params.get(key) if key != "page_token" else page_token
            if value:
                kwargs[key] = value
        data = serialize_result(call(**kwargs))
        names.extend(extract(data))
        page_token = data.get("next_page_token") or ""
        if not page_token:
            break
    return names


def list_teams(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    """List team usernames usable as CreateProjectRequest.team_name."""
    params = params or {}
    try:
        client = setup_client(config["host"], config["api_key"])
        source = None
        team_names: List[str] = []

        try:
            team_names = _collect_team_names(
                client, "list_teams_accelerator_quota", _names_from_accelerator_quota, params
            )
            if team_names:
                source = "list_teams_accelerator_quota"
        except ApiException:
            team_names = []

        if not team_names:
            team_names = _collect_team_names(
                client, "list_groups_quota", _names_from_groups_quota, params
            )
            if team_names:
                source = "list_groups_quota"

        unique_teams = sorted(set(team_names))
        if not unique_teams:
            return {
                "success": False,
                "message": (
                    "No teams found via quota APIs. Set CAI_WORKBENCH_TEAM or pass "
                    "team_name to create_project_tool (team username, e.g. Team1)."
                ),
                "data": {"teams": [], "source": source},
            }

        return {
            "success": True,
            "message": "list_teams ok",
            "data": {"teams": unique_teams, "source": source},
        }
    except ApiException as e:
        return {"success": False, "message": f"API error: {e.status} - {e.body}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
