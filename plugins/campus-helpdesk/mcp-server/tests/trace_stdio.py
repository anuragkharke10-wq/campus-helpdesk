"""Drive server.py over stdio with raw JSON-RPC and record every message.

Usage:  uv run python tests/trace_stdio.py [output.jsonl]

Writes one JSON object per line: {"dir": "client->server" | "server->client", "msg": {...}}.
Uses the initialize handshake (protocol 2025-11-25) because that is the flow the assignment asks
to annotate; the SDK also speaks the stateless 2026-07-28 revision.
"""

import json
import subprocess
import sys
from pathlib import Path

SERVER = Path(__file__).resolve().parent.parent / "server.py"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("mcp_trace.jsonl")

proc = subprocess.Popen(
    [sys.executable, str(SERVER)],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1,
)
log = []


def send(msg):
    log.append({"dir": "client->server", "msg": msg})
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()


def recv():
    line = proc.stdout.readline()
    if not line:
        raise RuntimeError("server closed stdout; stderr:\n" + proc.stderr.read())
    msg = json.loads(line)
    log.append({"dir": "server->client", "msg": msg})
    return msg


def request(id_, method, params=None):
    msg = {"jsonrpc": "2.0", "id": id_, "method": method}
    if params is not None:
        msg["params"] = params
    send(msg)
    while True:  # skip any server notifications until our response arrives
        reply = recv()
        if reply.get("id") == id_:
            return reply


request(1, "initialize", {
    "protocolVersion": "2025-11-25",
    "capabilities": {"roots": {"listChanged": True}},
    "clientInfo": {"name": "trace-client", "version": "0.1.0"},
})
send({"jsonrpc": "2.0", "method": "notifications/initialized"})
request(2, "tools/list")
request(3, "tools/call", {"name": "get_timetable", "arguments": {"batch": "CSE-A", "day": "Monday"}})
request(4, "tools/call", {"name": "get_fee_status", "arguments": {"student_id": "NU2024CS017"}})
request(5, "resources/list")
request(6, "resources/read", {"uri": "campus://hostel/rules"})
# Failure cases
request(7, "tools/call", {"name": "get_fee_status", "arguments": {"student_id": "12345; DROP TABLE fees"}})
request(8, "tools/call", {"name": "get_timetable", "arguments": {"batch": "MECH-A", "day": "Monday"}})
request(9, "tools/call", {"name": "get_timetable", "arguments": {"batch": "CSE-A", "day": "Saturday"}})
request(10, "tools/call", {"name": "delete_student", "arguments": {}})

proc.stdin.close()
proc.wait(timeout=10)
OUT.write_text("\n".join(json.dumps(e) for e in log) + "\n", encoding="utf-8")
Path(str(OUT) + ".stderr.log").write_text(proc.stderr.read(), encoding="utf-8")
print(f"wrote {len(log)} messages to {OUT}")
