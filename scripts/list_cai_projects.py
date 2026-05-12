#!/usr/bin/env python3
"""List projects using cmlapi (same client as Cloudera AI Workbench).

Reads CAI_WORKBENCH_HOST and CAI_WORKBENCH_API_KEY from repo-root .env only.

Usage:
  .venv/bin/python scripts/list_cai_projects.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import cmlapi
from dotenv import dotenv_values

_REPO_ROOT = Path(__file__).resolve().parent.parent


def _normalize_host(host: str) -> str:
    host = host.strip().rstrip("/")
    if not host.startswith(("http://", "https://")):
        host = "https://" + host
    return host


def list_all_projects(client: cmlapi.CMLServiceApi) -> list:
    """Follow next_page_token until all pages are collected."""
    merged: list = []
    token = None
    while True:
        if token:
            resp = client.list_projects(page_token=token)
        else:
            resp = client.list_projects()
        batch = resp.projects or []
        merged.extend(batch)
        token = resp.next_page_token
        if not token:
            break
    return merged


def main() -> int:
    env = dotenv_values(_REPO_ROOT / ".env")
    api_url = _normalize_host(env.get("CAI_WORKBENCH_HOST") or "")
    api_key = env.get("CAI_WORKBENCH_API_KEY") or ""
    if not api_url or not api_key:
        print("Missing CAI_WORKBENCH_HOST or CAI_WORKBENCH_API_KEY in .env", file=sys.stderr)
        return 1

    api_client = cmlapi.default_client(url=api_url, cml_api_key=api_key)
    projects = list_all_projects(api_client)
    rows = []
    for p in projects:
        d = p.to_dict() if hasattr(p, "to_dict") else {}
        rows.append(
            {
                "id": d.get("id"),
                "name": d.get("name"),
                "owner": d.get("owner"),
            }
        )
    print(json.dumps({"count": len(rows), "projects": rows}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(1)
