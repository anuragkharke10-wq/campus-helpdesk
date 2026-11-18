#!/usr/bin/env python3
"""PreToolUse hook: block Write/Edit calls that target protected student records.

Protected: <project>/records/ and the Skill's timetable CSV.
Exit code 2 blocks the tool call; stderr is shown to Claude as the reason.
"""
import json
import os
import sys

PROTECTED_DIRS = ["records/"]
PROTECTED_FILES = ["skills/timetable-helper/assets/timetable.csv"]


def main():
    event = json.load(sys.stdin)
    path = event.get("tool_input", {}).get("file_path") or event.get("tool_input", {}).get("notebook_path", "")
    if any(path.startswith(d) for d in PROTECTED_DIRS) or any(path.endswith(f) for f in PROTECTED_FILES):
        print(f"Blocked by campus-helpdesk: '{path}' is a protected student-records path.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
