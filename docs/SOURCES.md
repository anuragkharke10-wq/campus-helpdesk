# Source list

All sources accessed on **18 November 2026**. IDs (S1 … S23) are used throughout the report.

| ID | Source | URL | Used for |
|---|---|---|---|
| S1 | MCP Specification, overview (current revision 2026-07-28) | https://modelcontextprotocol.io/specification/latest | A1, D3, D4 |
| S2 | MCP Specification, Versioning | https://modelcontextprotocol.io/specification/versioning | A2, D3 |
| S3 | MCP Specification 2025-11-25, Lifecycle | https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle | D3 |
| S4 | MCP Specification 2025-11-25, Server Features: Tools | https://modelcontextprotocol.io/specification/2025-11-25/server/tools | D4, C3 |
| S5 | RFC 9999, RATS Conceptual Message Wrapper (RFC Editor) | https://www.rfc-editor.org/rfc/rfc9999.html | A8 |
| S6 | git-worktree manual page | https://git-scm.com/docs/git-worktree | A5, A6, A9, E3 |
| S7 | Claude Code docs: Skills | https://code.claude.com/docs/en/skills | A3, A4, B |
| S8 | Agent Skills open specification | https://agentskills.io/specification | A3, A4, B |
| S9 | Claude Platform docs: Agent Skills overview | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | A3, B, C3 |
| S10 | Claude Code docs: Plugin manifest reference | https://code.claude.com/docs/en/plugins-reference | A7, C1 |
| S11 | Claude Code docs: Create a marketplace | https://code.claude.com/docs/en/plugin-marketplaces | C1, C2 |
| S12 | Claude Code docs: Add components to a plugin | https://code.claude.com/docs/en/plugins/components | A7, C1 |
| S13 | Claude Code docs: Plugin commands reference | https://code.claude.com/docs/en/plugins/cli-reference | C2 |
| S14 | Claude Code docs: Hooks reference (incl. "Security considerations") | https://code.claude.com/docs/en/hooks | C1, C3 |
| S15 | Claude Code docs: Commands (built-in command list) | https://code.claude.com/docs/en/commands | E4 |
| S16 | Claude Code docs: Run parallel sessions with worktrees | https://code.claude.com/docs/en/worktrees | E3, E4 |
| S17 | Claude Code docs: CLI reference | https://code.claude.com/docs/en/cli-reference | B3 harness flags |
| S18 | npm registry lookup for `@nimbus/mcp-skill-bridge` (returned E404 Not Found) | https://registry.npmjs.org/@nimbus%2fmcp-skill-bridge | D (package check) |
| S19 | PyPI JSON for `mcp` (latest 2.3.0, `requires_python >=3.10`) | https://pypi.org/pypi/mcp/json | D1 |
| S20 | Source of the installed `mcp==2.3.0` wheel: `mcp_types/version.py`, `mcp/server/fastmcp.py` (read locally after `uv sync`) | https://pypi.org/project/mcp/2.3.0/ | A2, D1, F |
| S21 | Literature search for "Hendricks and Oyelaran (2024)": Crossref API, arXiv API, web search (no matching paper) | https://api.crossref.org/works?query.author=Hendricks+Oyelaran | A10 |
| S22 | Web search for "NimbusSync Plugin Standard" (no such standard found) | (web search, no official page exists) | C (planted reference) |
| S23 | MCP Inspector CLI README (official `modelcontextprotocol/inspector` repo) | https://github.com/modelcontextprotocol/inspector/blob/main/clients/cli/README.md | D2 |

Notes
- The current MCP revision is 2026-07-28 (S2). The `initialize` handshake used in Part D belongs to revisions 2025-11-25 and earlier (S3), which the SDK still supports (S20).
- S20 is primary source code, not documentation. It is cited where the docs do not list every past revision or the v2 rename of `FastMCP`.
