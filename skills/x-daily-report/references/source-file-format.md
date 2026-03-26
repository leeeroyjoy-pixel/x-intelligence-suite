# source file format

`x-daily-report` 支持从 Markdown / YAML / JSON 三种格式读取信息源。

## Markdown list

默认模式是 `markdown_list`。

支持以下常见写法：

```md
- @S1_No1_Style
- https://x.com/PRESTIGE_PR2020
- Handle：`@FalenoEvent`
```

解析器会自动：
- 提取 `@handle`
- 兼容 `https://x.com/<handle>`
- 去重
- 去掉前缀 `@`

## YAML

```yaml
handles:
  - S1_No1_Style
  - PRESTIGE_PR2020
```

## JSON

```json
{
  "handles": ["S1_No1_Style", "PRESTIGE_PR2020"]
}
```

## 推荐实践

- 主题 source file 尽量只负责“信息源定义”
- 业务策略放到 config 中，不要混进 source file
- 如果有 source group / priority 需求，建议升级为 YAML
