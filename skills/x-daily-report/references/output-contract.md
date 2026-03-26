# output contract

`x-daily-report` 默认输出 4 类产物：

1. Markdown 主文档
2. `summary.json`
3. 媒体 manifest JSON
4. distribution summary 文本

## 1. Markdown 主文档

- 面向人阅读
- 包含标题、时间窗口、核心条目、链接、摘要、媒体嵌入

## 2. summary.json

示例：

```json
{
  "status": "success",
  "profile": "example-report",
  "run_date": "2026-03-26",
  "content_date": "2026-03-25",
  "item_count": 6,
  "report_path": "outputs/2026-03-26/X日报-2026-03-25.md",
  "media_manifest_path": "outputs/2026-03-26/media-manifest.json",
  "distribution_summary_path": "outputs/2026-03-26/distribution-summary.txt",
  "highlights": [
    {
      "handle": "S1_No1_Style",
      "post_id": "2036639272758108397",
      "url": "https://x.com/i/status/2036639272758108397",
      "media_count": 1
    }
  ],
  "warnings": [],
  "errors": []
}
```

## 3. media manifest

每项至少包含：
- `handle`
- `post_id`
- `url`
- `files`
- `image_count`
- `video_count`
- `status`

## 4. distribution summary

- 面向渠道分发
- 纯文本短摘要
- 可直接被上游发布链消费

## 契约要求

- 若 `status=success`，主文档和 `summary.json` 必须存在
- `summary.json` 中的路径字段必须指向实际产物
- `highlights` 的数量不能超过最终保留条目数
