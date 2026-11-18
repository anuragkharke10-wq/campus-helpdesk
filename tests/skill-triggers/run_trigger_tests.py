#!/usr/bin/env python3
"""Run the Part B trigger tests against the timetable-helper Skill with Claude Code.

Usage (from the repo root, with the Claude Code CLI installed and logged in):

    python3 tests/skill-triggers/run_trigger_tests.py --variant v3-final
    python3 tests/skill-triggers/run_trigger_tests.py --variant v1-broad
    python3 tests/skill-triggers/run_trigger_tests.py --variant v2-narrow
    python3 tests/skill-triggers/run_trigger_tests.py --variant v3-final --dry-run   # print commands only

For each prompt it copies the plugin to a temp dir, swaps in the chosen description, and runs
    claude -p "<prompt>" --plugin-dir <copy> --output-format stream-json --verbose
           --max-turns 4 --no-session-persistence --allowedTools "Skill" "Bash(python3:*)" "Read"
then records whether a Skill tool call naming timetable-helper appears in the stream.
Raw stream logs are kept in evidence/partB_triggers/<variant>/<id>.jsonl so every verdict
can be checked by hand. This script decides "triggered" from the log; it does not judge answer quality.
"""
import argparse
import csv
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "plugins" / "campus-helpdesk"
SPEC = json.loads((Path(__file__).parent / "prompts.json").read_text())


def make_variant(tmp: Path, description: str) -> Path:
    dest = tmp / "campus-helpdesk"
    shutil.copytree(PLUGIN, dest, ignore=shutil.ignore_patterns(".venv", "__pycache__"))
    skill = dest / "skills" / "timetable-helper" / "SKILL.md"
    lines = skill.read_text().splitlines()
    lines = [f"description: {description}" if l.startswith("description:") else l for l in lines]
    skill.write_text("\n".join(lines) + "\n")
    return dest


def skill_called(stream_lines) -> bool:
    for line in stream_lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        for block in (event.get("message") or {}).get("content") or []:
            if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                if "timetable-helper" in json.dumps(block.get("input", {})):
                    return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=sorted(SPEC["descriptions"]), default="v3-final")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    out_dir = ROOT / "evidence" / "partB_triggers" / args.variant
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        plugin_copy = make_variant(Path(tmp), SPEC["descriptions"][args.variant])
        for p in SPEC["prompts"]:
            cmd = ["claude", "-p", p["text"], "--plugin-dir", str(plugin_copy),
                   "--output-format", "stream-json", "--verbose", "--max-turns", "4",
                   "--no-session-persistence", "--allowedTools", "Skill", "Bash(python3:*)", "Read"]
            if args.dry_run:
                print(" ".join(repr(c) if " " in c else c for c in cmd))
                continue
            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=tmp, timeout=300)
            (out_dir / f"{p['id']}.jsonl").write_text(proc.stdout)
            lines = proc.stdout.splitlines()
            final = next((json.loads(l).get("result", "") for l in reversed(lines)
                          if l.startswith("{") and '"type":"result"' in l.replace(" ", "")), "")
            row = {"variant": args.variant, "id": p["id"], "kind": p["kind"],
                   "triggered": skill_called(lines), "exit": proc.returncode,
                   "answer_excerpt": final[:200].replace("\n", " ")}
            results.append(row)
            print(f"{row['id']:4} {row['kind']:20} triggered={row['triggered']}  exit={row['exit']}")
    if results:
        with open(out_dir / "results.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(results[0]))
            w.writeheader()
            w.writerows(results)
        print(f"results -> {out_dir / 'results.csv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
