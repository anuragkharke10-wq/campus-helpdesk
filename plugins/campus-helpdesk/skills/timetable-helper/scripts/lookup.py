#!/usr/bin/env python3
"""Look up rows in the timetable-helper CSV.

Exit codes: 0 = rows found, 2 = bad input (unknown batch/day), 3 = valid query but no rows.
Standard library only, so it runs on any Python 3.9+.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "assets" / "timetable.csv"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def load_rows(path=CSV_PATH):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def normalise_batch(value):
    """'cse a', 'CSE_A', 'cse-a' -> 'CSE-A'."""
    m = re.fullmatch(r"\s*([A-Za-z]+)[\s_-]*([A-Za-z0-9]+)\s*", value or "")
    return f"{m.group(1).upper()}-{m.group(2).upper()}" if m else (value or "").strip().upper()


def normalise_day(value):
    v = (value or "").strip().rstrip(".").lower()
    for day in DAYS:
        if len(v) >= 3 and day.lower().startswith(v):
            return day
    return None


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--batch", help="e.g. CSE-A")
    p.add_argument("--day", help="e.g. Monday or Mon")
    p.add_argument("--course", help="course code or part of the course name, e.g. CS307 or networks")
    p.add_argument("--list-batches", action="store_true")
    p.add_argument("--csv", default=str(CSV_PATH), help=argparse.SUPPRESS)
    args = p.parse_args(argv)

    rows = load_rows(args.csv)
    batches = sorted({r["batch"] for r in rows})

    if args.list_batches:
        print(json.dumps({"batches": batches}))
        return 0
    if not args.batch:
        print(json.dumps({"error": "batch is required", "valid_batches": batches}))
        return 2

    batch = normalise_batch(args.batch)
    if batch not in batches:
        print(json.dumps({"error": f"unknown batch '{args.batch}'", "valid_batches": batches}))
        return 2
    matches = [r for r in rows if r["batch"] == batch]

    if args.day:
        day = normalise_day(args.day)
        if day is None:
            print(json.dumps({"error": f"unrecognised day '{args.day}'", "valid_days": DAYS[:5]}))
            return 2
        matches = [r for r in matches if r["day"] == day]

    if args.course:
        q = args.course.strip().lower()
        matches = [r for r in matches if q in r["course_code"].lower() or q in r["course_name"].lower()]

    matches.sort(key=lambda r: (DAYS.index(r["day"]), r["start"]))
    print(json.dumps({"batch": batch, "count": len(matches), "rows": matches}, indent=2))
    return 0 if matches else 3


if __name__ == "__main__":
    sys.exit(main())
