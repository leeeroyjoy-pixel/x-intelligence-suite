#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

HANDLE_PATTERNS = [
    re.compile(r'Handle：`@([^`]+)`'),
    re.compile(r'@([A-Za-z0-9_]+)'),
    re.compile(r'https?://x\.com/([A-Za-z0-9_]+)'),
]


def load_source_file(path: Path, source_type: str):
    text = path.read_text()
    if source_type == 'markdown_list':
        return text
    if source_type == 'json':
        return json.loads(text)
    if source_type == 'yaml':
        if yaml is None:
            raise RuntimeError('PyYAML is required to read YAML source files')
        return yaml.safe_load(text)
    raise ValueError(f'unsupported source_type: {source_type}')


def extract_handles(raw_source, source_type: str) -> list[str]:
    if source_type == 'markdown_list':
        found = []
        for pattern in HANDLE_PATTERNS:
            found.extend(pattern.findall(raw_source))
        return found
    if source_type in {'json', 'yaml'}:
        if isinstance(raw_source, dict):
            return list(raw_source.get('handles', []) or [])
        if isinstance(raw_source, list):
            return list(raw_source)
    return []


def normalize_sources(handles: list[str], include_handles: list[str], exclude_handles: list[str], dedupe: bool, priority_handles: list[str] | None = None) -> list[dict]:
    priority_handles = priority_handles or []
    items = [h.lstrip('@').strip() for h in handles + include_handles if h and h.strip()]
    excluded = {h.lstrip('@').strip() for h in exclude_handles if h}
    items = [h for h in items if h not in excluded]
    if dedupe:
        seen = set()
        uniq = []
        for h in items:
            if h not in seen:
                uniq.append(h)
                seen.add(h)
        items = uniq
    ordered = [h for h in priority_handles if h in items] + [h for h in items if h not in priority_handles]
    return [{'handle': h, 'platform': 'x', 'group': None, 'priority': i if h in priority_handles else None} for i, h in enumerate(ordered)]
