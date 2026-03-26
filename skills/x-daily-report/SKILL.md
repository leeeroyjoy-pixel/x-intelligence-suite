---
name: x-daily-report
description: >
  Generates a configurable daily X report from a source list. Collects posts from
  selected X accounts, filters and ranks items within a time window, downloads media,
  and outputs Markdown report artifacts plus machine-readable summaries. Use when
  user asks to "generate X daily report", "build Twitter/X digest", "抓取 X 账号日报",
  "生成推特日报", "按账号池做昨日汇总", "监控一组 X 信息源并输出日报", or needs a reusable
  X-source-driven reporting workflow.
version: 1.0.0
license: MIT
allowed-tools: [Bash, Read, Write]
---

## 概述

`x-daily-report` 用于从一组 X 信息源生成结构化日报。

它适用于以下任务：
- 已有一组账号池 / 信息源
- 需要按时间窗口抓取内容
- 需要筛选出最值得保留的条目
- 需要输出本地 Markdown 日报
- 需要同步生成 `summary.json`、媒体清单、分发摘要

这个 skill 不是一次性 prompt，而是一条可配置、可复用、可落盘的日报工作流。

## 何时使用

在以下场景使用：
- 用户要求“生成一份 X / Twitter 日报”
- 用户已有一组固定账号，希望每日自动汇总
- 用户需要“按昨天 / 最近 24 小时 / 自定义窗口”筛选 X 内容
- 用户需要将结果落盘到本地目录或知识库
- 用户需要 Markdown 主文档 + 机器可读摘要 + 媒体归档
- 用户希望同一套技能通过不同配置复用于不同主题，如 AI、Crypto、品牌监控、成人资讯

## 输入要求

支持以下输入来源：

1. 一个主题配置文件（推荐）
   - 位于 `configs/*.yaml`
   - 定义信息源、时间窗口、选条规则、媒体策略、输出规则

2. 一个信息源文件
   - Markdown / YAML / JSON
   - 至少包含要监控的 X handles

3. 可选运行时覆盖参数
   - 运行日期
   - 时间窗口模式
   - dry-run
   - 输出目录

## 工作流程

### Phase 1: 配置解析
1. 读取配置文件
2. 合并运行时覆盖参数
3. 计算内容窗口与输出日期
4. 校验必要字段

### Phase 2: 信息源解析
1. 读取 source file
2. 提取并规范化 X handles
3. 应用 include/exclude 规则
4. 去重并保留优先级顺序

### Phase 3: 内容采集与筛选
1. 按 source 抓取候选 posts
2. 过滤回复、转推、重复主题或噪声内容
3. 按规则或打分选出最终条目
4. 为每条内容生成统一结构化对象

### Phase 4: 媒体归档
1. 下载条目对应媒体
2. 生成媒体文件路径清单
3. 按配置决定正文嵌图/嵌视频策略
4. 生成媒体 manifest

### Phase 5: 报告生成
1. 生成 Markdown 主日报
2. 生成 `summary.json`
3. 生成短分发摘要
4. 校验产物一致性并返回结果

## 关键规则

- 先落盘，再允许后续分发链消费
- 主文档缺失时必须视为失败
- `summary.json` 必须与实际产物一致
- 配置优先于默认值
- 视频默认不嵌正文，除非配置明确开启
- 输出目录、时间窗口、信息源均应来自配置层，而不是硬编码主题值
- 该 skill 负责生成产物；发布动作应由上游发布链或其他 skill 执行

## 输出契约

默认输出包括：
- 1 个 Markdown 主文档
- 1 个 `summary.json`
- 1 个媒体 manifest
- 1 份可直接用于分发的短摘要文本

详细字段见：
- `references/config-schema.md`
- `references/source-file-format.md`
- `references/output-contract.md`

## 推荐调用方式

```bash
python skills/x-daily-report/scripts/run_x_daily_report.py \
  --config skills/x-daily-report/configs/jav-news.yaml \
  --date 2026-03-26 \
  --dry-run
```

或：

```bash
python skills/x-daily-report/scripts/run_x_daily_report.py \
  --config skills/x-daily-report/configs/ai-news.yaml \
  --window-mode last_24h
```

## 不要这样使用

- 不要把具体主题写死在脚本里
- 不要把一次性 prompt 当成 skill
- 不要在没有产物校验的情况下直接分发
- 不要把信息源、标题、输出目录等主题策略直接硬编码在执行器中
