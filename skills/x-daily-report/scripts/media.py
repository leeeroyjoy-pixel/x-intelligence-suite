#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import subprocess


def download_media_for_item(item: dict, runtime: dict, config: dict) -> dict:
    outdir = Path(runtime['output_dir']) / config['media'].get('media_dir_name', 'tweet_screens') / f"{item['handle']}_{item['post_id']}"
    outdir.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(
        ['opencli', 'twitter', 'download', '--tweet-url', item['url'], '--output', str(outdir), '-f', 'json'],
        capture_output=True,
        text=True,
    )
    files = [str(x) for x in sorted(outdir.rglob('*')) if x.is_file()]
    data = None
    if p.stdout.strip():
        try:
            data = json.loads(p.stdout)
        except Exception:
            data = None
    return {
        'handle': item['handle'],
        'post_id': item['post_id'],
        'url': item['url'],
        'files': files,
        'image_count': len([f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]),
        'video_count': len([f for f in files if f.lower().endswith(('.mp4', '.mov', '.m4v', '.webm'))]),
        'status': 'success' if p.returncode == 0 else 'failed',
        'raw': data,
    }


def resolve_embedded_media(item: dict, config: dict) -> list[str]:
    embedded = []
    if config['media'].get('embed_images', True):
        embedded.extend([f for f in item.get('media_files', []) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
    if config['media'].get('embed_videos', False):
        embedded.extend([f for f in item.get('media_files', []) if f.lower().endswith(('.mp4', '.mov', '.m4v', '.webm'))])
    limit = config['media'].get('max_embedded_images_per_item', 8)
    return embedded[:limit]


def attach_media(report_items: list[dict], runtime: dict, config: dict) -> tuple[list[dict], list[dict]]:
    manifest = []
    if not config['media'].get('download_media', True):
        return report_items, manifest
    for item in report_items:
        media_meta = download_media_for_item(item, runtime, config)
        item['media_files'] = media_meta['files']
        item['embedded_media_files'] = resolve_embedded_media(item, config)
        manifest.append(media_meta)
    return report_items, manifest
