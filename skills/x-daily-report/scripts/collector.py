#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess


def _run_json(cmd: list[str]) -> list[dict]:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or f'command failed: {cmd}')
    return json.loads(p.stdout)


def fetch_posts_for_source(source: dict, runtime: dict, config: dict) -> list[dict]:
    limit = str(config.get('selection', {}).get('fetch_limit', 8) or 8)
    items = _run_json(['opencli', 'twitter', 'search', f'from:{source["handle"]}', '-f', 'json', '--limit', limit])
    out = []
    for it in items:
        out.append({
            'handle': source['handle'],
            'post_id': it.get('id', ''),
            'url': it.get('url', ''),
            'text': it.get('text', ''),
            'created_at': it.get('created_at'),
            'likes': it.get('likes', 0),
            'views': it.get('views', ''),
            'is_reply': str(it.get('text', '')).startswith('@'),
            'is_retweet': False,
            'media': it.get('media', []),
            'raw': it,
        })
    return out


def collect_candidates(sources: list[dict], runtime: dict, config: dict) -> tuple[list[dict], list[str]]:
    candidates = []
    warnings = []
    for source in sources:
        try:
            candidates.extend(fetch_posts_for_source(source, runtime, config))
        except Exception as e:
            warnings.append(f'collect failed for @{source["handle"]}: {e}')
            if runtime.get('fail_fast'):
                raise
    return candidates, warnings
