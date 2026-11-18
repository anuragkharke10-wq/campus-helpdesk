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

Tests and traces (run from `plugins/campus-helpdesk/mcp-server`):

```bash
uv run python tests/test_server.py                                    # official SDK client, both protocol modes
uv run python tests/trace_stdio.py ../../../evidence/partD_mcp_trace.jsonl   # raw JSON-RPC trace
npx @modelcontextprotocol/inspector --cli uv run python server.py --method tools/list
```

Tools: `get_timetable(batch, day)`, `get_fee_status(student_id)`. Resource: `campus://hostel/rules`.

## Install the plugin in Claude Code

From the folder that contains this repository:

```bash
claude plugin validate ./campus-helpdesk
claude plugin marketplace add ./campus-helpdesk
claude plugin install campus-helpdesk@nimbus-campus-tools
claude plugin list
claude plugin details campus-helpdesk
```

In a session, `/campus-helpdesk:timetable CSE-A Monday` runs the command and `/mcp` shows `plugin:campus-helpdesk:campus`.
Remove it with `claude plugin uninstall campus-helpdesk@nimbus-campus-tools` and `claude plugin marketplace remove nimbus-campus-tools`.
The MCP entry runs `uv`, so `uv` must be on your `PATH`.

## Other checks

```bash
python3 plugins/campus-helpdesk/skills/timetable-helper/scripts/lookup.py --batch CSE-A --day Monday
python3 plugins/campus-helpdesk/hooks/test_protect_records.py
python3 tests/skill-triggers/run_trigger_tests.py --variant v3-final      # needs the Claude Code CLI, logged in
```

The report, prompt log and source list are in `docs/`.

## Project status

| Workstream | Status |
|---|---|
| Skill tests | 7 trigger prompts + 3 description variants (tests/skill-triggers) |
| MCP server tests | SDK client test + raw JSON-RPC trace (mcp-server/tests) |
| Hook path fix | done: absolute, `..` and case-variant paths blocked (hooks/test_protect_records.py) |
