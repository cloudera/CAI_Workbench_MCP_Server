"""List news feeds by category."""

import requests
from typing import Any, Dict
from urllib.parse import quote

from .http_helpers import auth_headers, normalize_host, pick_query, request_error

_Q = ("page_size", "page_token")


def list_news_feeds(config: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        cat = params.get("category")
        if not cat:
            return {"success": False, "message": "Missing category (path segment for /api/v2/newsfeeds/{category})"}
        host = normalize_host(config.get("host", ""))
        api_key = config.get("api_key")
        if not api_key:
            return {"success": False, "message": "Missing api_key in configuration"}
        q = pick_query(params or {}, _Q)
        r = requests.get(
            f"{host}/api/v2/newsfeeds/{quote(cat, safe='')}",
            headers=auth_headers(api_key),
            params=q,
            timeout=60,
        )
        r.raise_for_status()
        return {"success": True, "message": "list_news_feeds ok", "data": r.json()}
    except Exception as e:
        return request_error("list_news_feeds", e)
