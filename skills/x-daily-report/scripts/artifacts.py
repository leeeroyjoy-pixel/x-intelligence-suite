#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json


def write_report(markdown: str, paths: dict) -> str:
    path = Path(paths['report_path'])
    path.write_text(markdown)
    return str(path)


def write_distribution_summary(summary_text: str, paths: dict) -> str:
    path = Path(paths['distribution_summary_path'])
    path.write_text(summary_text)
    return str(path)


def write_summary_json(report_items: list[dict], runtime: dict, config: dict, paths: dict, warnings: list[str] | None = None, errors: list[str] | None = None) -> str:
    warnings = warnings or []
    errors = errors or []
    data = {
        'status': 'success' if not errors else 'failed',
        'profile': runtime['profile_name'],
        'run_date': runtime['run_date'],
        'content_date': runtime['content_date'],
        'item_count': len(report_items),
        'report_path': paths['report_path'],
        'media_manifest_path': paths['media_manifest_path'],
        'distribution_summary_path': paths['distribution_summary_path'],
        'highlights': [
            {
                'handle': item['handle'],
                'post_id': item['post_id'],
                'url': item['url'],
                'media_count': len([f for f in item.get('media_files', []) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]),
            }
            for item in report_items
        ],
        'warnings': warnings,
        'errors': errors,
    }
    path = Path(paths['summary_json_path'])
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    return str(path)


def write_media_manifest(manifest: list[dict], paths: dict) -> str:
    path = Path(paths['media_manifest_path'])
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    return str(path)


def validate_artifacts(paths: dict, config: dict) -> list[str]:
    errors = []
    if config['output'].get('write_markdown', True) and not Path(paths['report_path']).exists():
        errors.append('missing report_path')
    if config['output'].get('write_summary_json', True) and not Path(paths['summary_json_path']).exists():
        errors.append('missing summary_json_path')
    if config['output'].get('write_media_manifest', True) and not Path(paths['media_manifest_path']).exists():
        errors.append('missing media_manifest_path')
    if config['output'].get('write_distribution_summary', True) and not Path(paths['distribution_summary_path']).exists():
        errors.append('missing distribution_summary_path')
    return errors


def build_run_result(paths: dict, report_items: list[dict], manifest: list[dict], warnings: list[str], errors: list[str], runtime: dict) -> dict:
    summary_text = ''
    summary_path = Path(paths['distribution_summary_path'])
    if summary_path.exists():
        summary_text = summary_path.read_text()
    return {
        'status': 'success' if not errors else 'failed',
        'profile': runtime['profile_name'],
        'run_date': runtime['run_date'],
        'content_date': runtime['content_date'],
        'item_count': len(report_items),
        'report_path': paths['report_path'],
        'summary_json_path': paths['summary_json_path'],
        'media_manifest_path': paths['media_manifest_path'],
        'distribution_summary': summary_text,
        'warnings': warnings,
        'errors': errors,
        'manifest_count': len(manifest),
    }
