#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

from config_loader import load_config, merge_cli_overrides, resolve_path, validate_config
from source_parser import load_source_file, extract_handles, normalize_sources
from collector import collect_candidates
from selector import filter_candidates, select_items, build_report_items
from media import attach_media
from renderer import resolve_output_paths, render_markdown, build_distribution_summary
from artifacts import (
    write_report,
    write_summary_json,
    write_media_manifest,
    write_distribution_summary,
    validate_artifacts,
    build_run_result,
)


def parse_cli_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description='Generate a configurable daily X report')
    p.add_argument('--config', required=True)
    p.add_argument('--date')
    p.add_argument('--window-mode', choices=['yesterday', 'today_so_far', 'last_24h', 'custom'])
    p.add_argument('--window-start')
    p.add_argument('--window-end')
    p.add_argument('--output-root')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--max-items', type=int)
    p.add_argument('--source-file')
    p.add_argument('--emit-summary', action='store_true')
    p.add_argument('--no-media', action='store_true')
    p.add_argument('--embed-videos', action='store_true')
    p.add_argument('--profile-name')
    p.add_argument('--verbose', action='store_true')
    p.add_argument('--dump-resolved-config', action='store_true')
    p.add_argument('--fail-fast', action='store_true')
    return p.parse_args()


def resolve_runtime_context(config: dict, base_dir: Path, args: argparse.Namespace) -> dict:
    tz = config['profile'].get('timezone', 'Asia/Shanghai')
    now = datetime.now()
    mode = config['window'].get('mode', 'yesterday')
    content_date = config['window'].get('content_date')
    if mode == 'yesterday' and not content_date:
        content_date = (now - timedelta(days=1)).strftime('%Y-%m-%d')
    elif mode == 'today_so_far' and not content_date:
        content_date = now.strftime('%Y-%m-%d')
    elif mode == 'last_24h' and not content_date:
        content_date = now.strftime('%Y-%m-%d')
    elif not content_date:
        content_date = now.strftime('%Y-%m-%d')
    run_date = now.strftime('%Y-%m-%d')
    if config['window'].get('output_date_mode') == 'content_date':
        run_date = content_date

    output_root = resolve_path(config['output']['output_root'], base_dir)
    output_dir = output_root / config['output'].get('output_subdir_pattern', '{run_date}').format(run_date=run_date, content_date=content_date)
    report_filename = config['output']['report_filename_pattern'].format(run_date=run_date, content_date=content_date)
    title = config['output']['title_template'].format(run_date=run_date, content_date=content_date)
    return {
        'profile_name': config['profile']['name'],
        'timezone': tz,
        'run_date': run_date,
        'content_date': content_date,
        'window_start': config['window'].get('window_start'),
        'window_end': config['window'].get('window_end'),
        'output_dir': str(output_dir),
        'report_filename': report_filename,
        'title': title,
        'dry_run': bool(config['publish'].get('dry_run', False)),
        'verbose': bool(args.verbose),
        'fail_fast': bool(args.fail_fast),
    }


def main() -> int:
    args = parse_cli_args()
    config, base_dir = load_config(args.config)
    config = merge_cli_overrides(config, vars(args))
    validate_config(config)
    runtime = resolve_runtime_context(config, base_dir, args)

    if args.dump_resolved_config:
        print(json.dumps(config, ensure_ascii=False, indent=2))

    source_path = resolve_path(config['sources']['source_file'], base_dir)
    raw_source = load_source_file(source_path, config['sources'].get('source_type', 'markdown_list'))
    handles = extract_handles(raw_source, config['sources'].get('source_type', 'markdown_list'))
    sources = normalize_sources(
        handles,
        config['sources'].get('include_handles', []) or [],
        config['sources'].get('exclude_handles', []) or [],
        bool(config['sources'].get('dedupe_sources', True)),
        config['sources'].get('priority_handles', []) or [],
    )

    candidates, warnings = collect_candidates(sources, runtime, config)
    filtered = filter_candidates(candidates, config, runtime)
    selected = select_items(filtered, config)
    report_items = build_report_items(selected, config)
    report_items, manifest = attach_media(report_items, runtime, config)

    paths = resolve_output_paths(runtime, config)
    markdown = render_markdown(report_items, runtime, config)
    distribution_summary = build_distribution_summary(report_items, runtime, config, paths['report_path'])

    if config['output'].get('write_markdown', True):
        write_report(markdown, paths)
    if config['output'].get('write_distribution_summary', True):
        write_distribution_summary(distribution_summary, paths)
    if config['output'].get('write_media_manifest', True):
        write_media_manifest(manifest, paths)
    errors = validate_artifacts(paths, config)
    if config['output'].get('write_summary_json', True):
        write_summary_json(report_items, runtime, config, paths, warnings=warnings, errors=errors)
        errors = validate_artifacts(paths, config)

    result = build_run_result(paths, report_items, manifest, warnings, errors, runtime)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if config['publish'].get('emit_stdout_summary', False):
        print('\n---DISTRIBUTION_SUMMARY---\n' + result.get('distribution_summary', ''))
    return 0 if result['status'] == 'success' else 1


if __name__ == '__main__':
    raise SystemExit(main())
