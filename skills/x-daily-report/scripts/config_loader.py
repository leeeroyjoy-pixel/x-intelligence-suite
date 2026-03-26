#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


def _deep_update(base: dict, patch: dict) -> dict:
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_update(base[k], v)
        else:
            base[k] = v
    return base


def load_config(config_path: str) -> tuple[dict, Path]:
    path = Path(config_path).expanduser().resolve()
    text = path.read_text()
    if path.suffix in {'.yaml', '.yml'}:
        if yaml is None:
            raise RuntimeError('PyYAML is required to read YAML config files')
        data = yaml.safe_load(text) or {}
    elif path.suffix == '.json':
        data = json.loads(text)
    else:
        raise ValueError(f'unsupported config file: {path}')
    return data, path.parent


def merge_cli_overrides(config: dict, args: dict) -> dict:
    merged = deepcopy(config)
    patch: dict = {}
    if args.get('date'):
        patch.setdefault('window', {})['content_date'] = args['date']
    if args.get('window_mode'):
        patch.setdefault('window', {})['mode'] = args['window_mode']
    if args.get('window_start'):
        patch.setdefault('window', {})['window_start'] = args['window_start']
    if args.get('window_end'):
        patch.setdefault('window', {})['window_end'] = args['window_end']
    if args.get('output_root'):
        patch.setdefault('output', {})['output_root'] = args['output_root']
    if args.get('max_items') is not None:
        patch.setdefault('selection', {})['max_items'] = args['max_items']
    if args.get('source_file'):
        patch.setdefault('sources', {})['source_file'] = args['source_file']
    if args.get('dry_run'):
        patch.setdefault('publish', {})['dry_run'] = True
    if args.get('emit_summary'):
        patch.setdefault('publish', {})['emit_stdout_summary'] = True
    if args.get('no_media'):
        patch.setdefault('media', {})['download_media'] = False
    if args.get('embed_videos'):
        patch.setdefault('media', {})['embed_videos'] = True
    if args.get('profile_name'):
        patch.setdefault('profile', {})['name'] = args['profile_name']
    return _deep_update(merged, patch)


def resolve_path(path_value: str, base_dir: Path) -> Path:
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = (base_dir / path).resolve()
    return path


def validate_config(config: dict) -> None:
    for key in ['profile', 'sources', 'window', 'selection', 'media', 'output', 'publish']:
        if key not in config:
            raise ValueError(f'missing top-level config section: {key}')
    if not config['sources'].get('source_file'):
        raise ValueError('sources.source_file is required')
    if not config['output'].get('output_root'):
        raise ValueError('output.output_root is required')
    if not config['output'].get('report_filename_pattern'):
        raise ValueError('output.report_filename_pattern is required')
    if not config['output'].get('title_template'):
        raise ValueError('output.title_template is required')
