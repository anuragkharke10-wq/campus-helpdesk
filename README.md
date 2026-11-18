# campus-helpdesk

Assignment 8, *Building and Auditing an AI-Agent Toolchain*, for the Nimbus Labs Campus Helpdesk Agent.
This repository is a Claude Code **plugin marketplace** (`nimbus-campus-tools`) that ships one plugin, `campus-helpdesk`.

> All data in this repository is **mock data**. There are no real students, passwords or API keys.

```
.claude-plugin/marketplace.json          marketplace catalogue (Part C)
plugins/campus-helpdesk/
├── .claude-plugin/plugin.json           plugin manifest (Part C)
├── skills/timetable-helper/             the Skill (Part B)
│   ├── SKILL.md
│   ├── references/columns.md            CSV column dictionary   (loaded on demand)
│   ├── references/edge-cases.md         edge cases              (loaded on demand)
│   ├── scripts/lookup.py                helper script           (executed, not loaded)
│   └── assets/timetable.csv             mock timetable
├── commands/timetable.md                /campus-helpdesk:timetable <batch> <day>
├── hooks/hooks.json                     PreToolUse hook config
├── hooks/protect_records.py             blocks writes to records/ and the timetable CSV
├── .mcp.json                            MCP server entry -> mcp-server/server.py
└── mcp-server/                          stdio MCP server, official Python SDK (Part D)
evidence/                                logs and traces used in the report
docs/                                    report, prompt log, sources
```

## Requirements

- Python 3.10+ (tested with 3.14.10 through `uv`) and [uv](https://docs.astral.sh/uv/)
- Claude Code CLI (for the plugin steps)
- git 2.39+ (for the worktree steps)

## Run the MCP server

```bash
cd plugins/campus-helpdesk/mcp-server
uv sync
uv run python server.py          # speaks MCP JSON-RPC on stdin/stdout; logs go to stderr
```

## Project status

| Workstream | Status |
|---|---|
| Skill tests | 7 trigger prompts + 3 description variants (tests/skill-triggers) |
| MCP server tests | not started |
| Hook path fix | not started |
