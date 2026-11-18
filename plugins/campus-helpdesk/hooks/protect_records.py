#!/usr/bin/env python3
"""PreToolUse hook: block Write/Edit calls that target protected student records.

Protected: <project>/records/ (any depth) and the Skill's timetable CSV.
Exit code 2 blocks the tool call; stderr is shown to Claude as the reason.

Claude Code always sends tool_input.file_path as an absolute path, so paths are resolved
(symlinks and '..' collapsed) and compared component-wise, case-insensitively, because the
default macOS file system ignores case ('Records/' is the same folder as 'records/').
"""
import json
import os
import sys
from pathlib import Path

PROTECTED_DIR_NAMES = {"records"}
PROTECTED_FILE_SUFFIX = ("skills", "timetable-helper", "assets", "timetable.csv")


def is_protected(raw_path: str, cwd: str) -> bool:
    if not raw_path:
        return False
    path = Path(raw_path)
    if not path.is_absolute():
        path = Path(cwd or os.getcwd()) / path
    parts = [p.lower() for p in Path(os.path.realpath(path)).parts]
    project = os.environ.get("CLAUDE_PROJECT_DIR")
    if project:
        root = [p.lower() for p in Path(os.path.realpath(project)).parts]
        inside = parts[: len(root)] == root
        if inside and PROTECTED_DIR_NAMES & set(parts[len(root):-1]):
            return True
    elif PROTECTED_DIR_NAMES & set(parts[:-1]):
        return True
    return tuple(parts[-4:]) == PROTECTED_FILE_SUFFIX


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("campus-helpdesk hook: could not parse hook input; blocking to be safe.", file=sys.stderr)
        return 2
    tool_input = event.get("tool_input") or {}
    raw = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if is_protected(raw, event.get("cwd", "")):
        print(f"Blocked by campus-helpdesk: '{raw}' is a protected student-records path. "
              "Ask the academic office to change these files.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
