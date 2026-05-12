"""Small helpers for Cloudera AI REST v2 requests."""

from __future__ import annotations

import json
from typing import Any, Dict

import cmlapi
import requests


def normalize_host(host: str) -> str:
    h = (host or "").strip()
    if h.startswith("https://https://"):
        h = h.replace("https://https://", "https://")
    if not h.startswith(("http://", "https://")):
        h = "https://" + h
    return h.rstrip("/")


def setup_client(host: str, api_key: str) -> cmlapi.CMLServiceApi:
    """Create a configured cmlapi client.

    Args:
        host: CAI Workbench host URL (raw — will be normalized).
        api_key: Bearer token for authentication.

    Returns:
        Ready-to-use CMLServiceApi instance.
    """
    config = cmlapi.Configuration()
    config.host = normalize_host(host)
    api_client = cmlapi.ApiClient(config)
    api_client.set_default_header("authorization", f"Bearer {api_key}")
    return cmlapi.CMLServiceApi(api_client)


def serialize_result(result) -> Any:
    """Convert a cmlapi response object to a JSON-safe dict."""
    if result is None:
        return None
    raw = result.to_dict() if hasattr(result, "to_dict") else result
    # Round-trip through JSON to handle datetime and other non-serializable types
    return json.loads(json.dumps(raw, default=str))


def auth_headers(api_key: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def pick_query(params: Dict[str, Any], keys: tuple) -> Dict[str, Any]:
    return {k: params[k] for k in keys if params.get(k) not in (None, "")}


def request_error(label: str, exc: BaseException) -> Dict[str, Any]:
    if isinstance(exc, requests.exceptions.RequestException):
        msg = str(exc)
        resp = getattr(exc, "response", None)
        if resp is not None:
            try:
                msg = f"{msg} - {json.dumps(resp.json())}"
            except Exception:
                msg = f"{msg} - {getattr(resp, 'text', '')}"
        return {"success": False, "message": f"{label}: {msg}"}
    return {"success": False, "message": f"{label}: {str(exc)}"}
