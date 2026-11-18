# timetable.csv column dictionary

| Column | Type | Allowed values / format | Notes |
|---|---|---|---|
| `batch` | string | `CSE-A`, `CSE-B`, `ECE-A` | Upper-case, hyphenated. Run `lookup.py --list-batches` for the live list. |
| `day` | string | `Monday` … `Friday` | Full English day name. There are **no Saturday or Sunday classes** in this file. |
| `start` | string | `HH:MM`, 24-hour | Local campus time (IST). |
| `end` | string | `HH:MM`, 24-hour | Always later than `start`. |
| `course_code` | string | e.g. `CS301`, `CS303L` | A trailing `L` means the lab component of the course with the same prefix. |
| `course_name` | string | free text | Use exactly as written; do not expand or rename. |
| `faculty` | string | free text | Mock names only. |
| `room` | string | `LH-xxx` lecture hall, `LAB-n` / `ECE-LAB-n` lab | |
| `session_type` | string | `Lecture`, `Lab`, `Tutorial` | |

All data in this file is **mock data** created for the assignment. It does not describe a real university.
