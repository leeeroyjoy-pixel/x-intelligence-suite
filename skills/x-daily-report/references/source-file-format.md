# source file format

`x-daily-report` 支持从 Markdown / YAML / JSON 三种格式读取信息源。

## Markdown list

默认模式是 `markdown_list`。

支持以下常见写法：

```md
- @example_handle_one
- https://x.com/example_handle_two
- Handle：`@example_handle_three`
```

解析器会自动：
- 提取 `@handle`
- 兼容 `https://x.com/<handle>`
- 去重
- 去掉前缀 `@`

## YAML

```yaml
handles:
  - example_handle_one
  - example_handle_two
```

## JSON

```json
{
  "handles": ["example_handle_one", "example_handle_two"]
}
```

## 推荐实践

- 主题 source file 尽量只负责“信息源定义”
- 业务策略放到 config 中，不要混进 source file
- 如果有 source group / priority 需求，建议升级为 YAML
