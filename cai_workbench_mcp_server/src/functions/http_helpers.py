"""Small helpers for Cloudera AI REST v2 requests."""

from __future__ import annotations

import json
import os
import ssl
from typing import Any, Dict, Union

import requests

_DEBIAN_CA_BUNDLE = "/etc/ssl/certs/ca-certificates.crt"


def normalize_host(host: str) -> str:
    h = (host or "").strip()
    if h.startswith("https://https://"):
        h = h.replace("https://https://", "https://")
    if not h.startswith(("http://", "https://")):
        h = "https://" + h
    return h.rstrip("/")


def system_ca_bundle() -> str | None:
    """Return the system CA bundle path when one is available."""
    for candidate in (
        os.environ.get("SSL_CERT_FILE"),
        os.environ.get("REQUESTS_CA_BUNDLE"),
        _DEBIAN_CA_BUNDLE,
    ):
        if candidate and os.path.exists(candidate):
            return candidate

    default = ssl.get_default_verify_paths().cafile
    if default and os.path.exists(default):
        return default
    return None


def requests_verify() -> Union[str, bool]:
    """CA bundle for requests; True keeps certifi default when no system bundle exists."""
    return system_ca_bundle() or True


def setup_client(host: str, api_key: str):
    """Create a configured cmlapi client.

    Args:
        host: CAI Workbench host URL (raw — will be normalized).
        api_key: Bearer token for authentication.

    Returns:
        Ready-to-use CMLServiceApi instance.
    """
    import cmlapi

    config = cmlapi.Configuration()
    config.host = normalize_host(host)
    ca_bundle = system_ca_bundle()
    if ca_bundle:
        config.ssl_ca_cert = ca_bundle
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
