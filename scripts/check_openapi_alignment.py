#!/usr/bin/env python3
"""Fail CI when documented API endpoints drift from live OpenAPI.

Checks method+path entries listed in api-reference.md against:
https://api.8k4protocol.com/openapi.json
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

DOC_PATH = Path(__file__).resolve().parent.parent / "api-reference.md"
OPENAPI_URL = "https://api.8k4protocol.com/openapi.json"

LINE_RE = re.compile(r"^\s*-\s*`(GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD)\s+([^`]+)`", re.IGNORECASE)
PARAM_RE = re.compile(r"\{[^}]+\}")


def normalize_path(path: str) -> str:
    path = path.strip()
    if "?" in path:
        path = path.split("?", 1)[0]
    if not path.startswith("/"):
        path = "/" + path
    path = PARAM_RE.sub("{}", path)
    return path


def fetch_openapi() -> dict:
    with urllib.request.urlopen(OPENAPI_URL, timeout=15) as resp:
        if resp.status != 200:
            raise RuntimeError(f"OpenAPI fetch failed: HTTP {resp.status}")
        return json.loads(resp.read().decode("utf-8"))


def collect_doc_endpoints(text: str) -> list[tuple[str, str, int]]:
    rows: list[tuple[str, str, int]] = []
    for i, raw in enumerate(text.splitlines(), start=1):
        m = LINE_RE.match(raw)
        if not m:
            continue
        method = m.group(1).upper()
        path = normalize_path(m.group(2))
        rows.append((method, path, i))
    return rows


def collect_openapi_endpoints(spec: dict) -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    for raw_path, methods in spec.get("paths", {}).items():
        norm_path = normalize_path(raw_path)
        if not isinstance(methods, dict):
            continue
        for method in methods.keys():
            out.add((method.upper(), norm_path))
    return out


def main() -> int:
    if not DOC_PATH.exists():
        print(f"ERROR: missing {DOC_PATH}")
        return 2

    doc_rows = collect_doc_endpoints(DOC_PATH.read_text(encoding="utf-8"))
    if not doc_rows:
        print("ERROR: no method+path endpoints found in api-reference.md")
        return 2

    spec = fetch_openapi()
    openapi = collect_openapi_endpoints(spec)

    missing: list[str] = []
    for method, path, line in doc_rows:
        if (method, path) not in openapi:
            missing.append(f"L{line}: `{method} {path}` not found in live OpenAPI")

    if missing:
        print("OpenAPI alignment failed:\n")
        print("\n".join(missing))
        return 1

    print(f"OpenAPI alignment OK ({len(doc_rows)} documented endpoints checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
