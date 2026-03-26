# x-daily-report config schema v1

`x-daily-report` 通过配置文件驱动不同主题日报。建议每个主题维护一份独立的 YAML 配置。

## 顶层结构

```yaml
profile:
sources:
window:
selection:
media:
output:
publish:
```

## 1. profile

```yaml
profile:
  name: example-report
  platform: x
  timezone: Asia/Shanghai
```

- `name` string, required: 配置名称
- `platform` string, default `x`
- `timezone` string, default `Asia/Shanghai`

## 2. sources

```yaml
sources:
  source_file: ./sources/example-handles.md
  source_type: markdown_list
  source_groups: []
  include_handles: []
  exclude_handles: []
  dedupe_sources: true
  priority_handles: []
```

- `source_file` string, required
- `source_type` enum: `markdown_list|yaml|json`
- `source_groups` string[]
- `include_handles` string[]
- `exclude_handles` string[]
- `dedupe_sources` boolean
- `priority_handles` string[]

## 3. window

```yaml
window:
  mode: yesterday
  content_date: null
  window_start: null
  window_end: null
  output_date_mode: run_date
```

- `mode` enum: `yesterday|today_so_far|last_24h|custom`
- `content_date` string|null, `YYYY-MM-DD`
- `window_start` string|null, ISO datetime
- `window_end` string|null, ISO datetime
- `output_date_mode` enum: `run_date|content_date`

## 4. selection

```yaml
selection:
  max_items: 6
  max_items_per_source: 2
  selection_mode: scored
  prefer_media_posts: true
  prefer_original_posts: true
  drop_replies: true
  drop_retweets: true
  drop_duplicate_topics: true
  priority_keywords: []
  exclude_keywords: []
```

## 5. media

```yaml
media:
  download_media: true
  embed_images: true
  embed_videos: false
  max_embedded_images_per_item: 8
  count_video_in_media_count: false
  media_dir_name: tweet_screens
  media_naming_mode: handle_tweetid
```

## 6. output

```yaml
output:
  output_root: ./outputs
  output_subdir_pattern: "{run_date}"
  report_filename_pattern: "X日报-{content_date}.md"
  write_markdown: true
  write_summary_json: true
  write_media_manifest: true
  write_distribution_summary: true
  distribution_summary_filename: distribution-summary.txt
  title_template: "X 日报｜{content_date}"
  markdown_template: default_report_template.md
```

## 7. publish

```yaml
publish:
  publish_enabled: false
  require_artifacts_before_publish: true
  require_summary_success: true
  fail_if_main_doc_missing: true
  dry_run: true
  emit_stdout_summary: true
```

## 推荐实践

- 每个主题维护单独 config
- 运行时只覆盖少量字段，如 `date`、`dry_run`
- 不要把 source file、输出目录、主题标题硬编码在脚本中
- 配置中表达业务策略，脚本中保留稳定执行逻辑
