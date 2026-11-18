#!/usr/bin/env python3
"""Feed sample PreToolUse events to protect_records.py and check the exit codes.

Usage: python3 plugins/campus-helpdesk/hooks/test_protect_records.py
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HOOK = Path(__file__).resolve().parent / "protect_records.py"

with tempfile.TemporaryDirectory() as tmp:
    project = Path(os.path.realpath(tmp)) / "campus"
    (project / "records").mkdir(parents=True)
    (project / "notes").mkdir()
    cases = [
        (str(project / "records" / "fees.json"), 2, "absolute path into records/"),
        ("records/fees.json", 2, "relative path into records/"),
        (str(project / "notes" / ".." / "records" / "x.json"), 2, "'..' traversal into records/"),
        (str(project / "Records" / "fees.json"), 2, "case variant on case-insensitive FS"),
        (str(project / "notes" / "todo.md"), 0, "ordinary file"),
        (str(project / "records-archive.md"), 0, "name merely starts with 'records'"),
        ("/opt/plugins/campus-helpdesk/skills/timetable-helper/assets/timetable.csv", 2, "timetable CSV"),
    ]
    failures = 0
    for path, expected, label in cases:
        event = {"hook_event_name": "PreToolUse", "tool_name": "Write", "cwd": str(project),
                 "tool_input": {"file_path": path, "content": "x"}}
        proc = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(event), text=True,
                              capture_output=True, env={**os.environ, "CLAUDE_PROJECT_DIR": str(project)})
        ok = proc.returncode == expected
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'}  exit={proc.returncode} expected={expected}  {label}")
    print("ALL HOOK CHECKS PASSED" if not failures else f"{failures} FAILED")
    sys.exit(1 if failures else 0)
