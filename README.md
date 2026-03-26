# x-intelligence-suite

A GitHub-publishable AgentSkills package for configurable X intelligence workflows.

## Included skill

- `x-daily-report`: generate a configurable daily X digest from a source list.

## Why this repo exists

This repo turns a one-off, hardcoded X daily report script into a reusable skill package:
- source-driven
- config-driven
- output-contract-driven
- GitHub-shareable

## Repo structure

```text
x-intelligence-suite/
├── .claude-plugin/plugin.json
├── skills/x-daily-report/
│   ├── SKILL.md
│   ├── scripts/
│   ├── references/
│   ├── assets/
│   └── configs/
├── sources/
└── outputs/
```

## Quick start

```bash
python skills/x-daily-report/scripts/run_x_daily_report.py \
  --config skills/x-daily-report/configs/jav-news.yaml \
  --dry-run
```

## Design goals

- reusable by other agents
- configurable without code edits
- stable output artifacts
- safe handoff to downstream publisher workflows

## Key files

- `skills/x-daily-report/SKILL.md`
- `skills/x-daily-report/references/config-schema.md`
- `skills/x-daily-report/references/output-contract.md`
- `skills/x-daily-report/configs/jav-news.yaml`


## Runtime requirements

- Python 3.9+
- `opencli` available in PATH
- Optional but recommended: `PyYAML` for YAML configs

Install Python dependency:

```bash
pip install -r requirements.txt
```

## Example run

```bash
python skills/x-daily-report/scripts/run_x_daily_report.py   --config skills/x-daily-report/configs/jav-news.json   --dry-run --no-media
```

Use `jav-news.yaml` when `PyYAML` is installed.
