"""End-to-end test of server.py through the official MCP Python SDK client over stdio.

Usage:  uv run python tests/test_server.py

Runs the same checks twice: once with the initialize handshake (mode="legacy",
protocol 2025-11-25) and once with the SDK default (mode="auto", which probes
server/discover and uses the stateless 2026-07-28 revision when the server supports it).
"""

import asyncio
import json
import sys
from pathlib import Path

from mcp import Client
from mcp.client.stdio import StdioServerParameters

SERVER = Path(__file__).resolve().parent.parent / "server.py"
PARAMS = StdioServerParameters(command=sys.executable, args=[str(SERVER)])


def text_of(result) -> str:
    return "".join(getattr(c, "text", "") for c in result.content)


async def run(mode: str) -> None:
    async with Client(PARAMS, mode=mode) as client:
        print(f"--- mode={mode}  negotiated protocol={client.session.protocol_version}")

        tools = await client.list_tools()
        names = sorted(t.name for t in tools.tools)
        print("tools/list ->", names)
        assert names == ["get_fee_status", "get_timetable"], names

        ok = await client.call_tool("get_timetable", {"batch": "CSE-A", "day": "Monday"})
        data = json.loads(text_of(ok))
        print("get_timetable(CSE-A, Monday) -> count", data["count"], [c["course_code"] for c in data["classes"]])
        assert not ok.is_error and data["count"] == 3

        fee = await client.call_tool("get_fee_status", {"student_id": "NU2024CS042"})
        print("get_fee_status(NU2024CS042) ->", json.loads(text_of(fee))["status"])
        assert json.loads(text_of(fee))["status"] == "UNPAID"

        bad = await client.call_tool("get_fee_status", {"student_id": "abc"})
        print("get_fee_status('abc') -> isError", bad.is_error)
        assert bad.is_error and "pattern" in text_of(bad)

        missing = await client.call_tool("get_fee_status", {"student_id": "NU2099CS999"})
        print("get_fee_status(NU2099CS999) -> isError", missing.is_error, "|", text_of(missing))
        assert missing.is_error

        resources = await client.list_resources()
        uris = [str(r.uri) for r in resources.resources]
        print("resources/list ->", uris)
        rules = await client.read_resource("campus://hostel/rules")
        first_line = rules.contents[0].text.splitlines()[0]
        print("resources/read ->", first_line)
        assert "Hostel Rules" in first_line


async def main() -> None:
    for mode in ("legacy", "auto"):
        await run(mode)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    asyncio.run(main())
