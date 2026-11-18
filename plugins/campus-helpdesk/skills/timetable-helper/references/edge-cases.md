# Edge cases

## Batch and day aliases
- "cse a", "CSE A", "cse-a" → `CSE-A`. The script normalises case, spaces and hyphens.
- "mon", "Mon." → `Monday`; the script accepts 3-letter prefixes.
- "today" / "tomorrow": the script does not know the date. Ask the student which day they mean,
  or work it out from the session's current date if it is available, and **say which day you assumed**.

## Weekends and holidays
- The CSV has no Saturday/Sunday rows. Answer "no classes are scheduled" rather than inventing any.
- The CSV has no holiday calendar. If asked "is there class on <festival>?", say the timetable
  does not cover holidays and point the student to the academic calendar.

## Unknown batch or course
- Unknown batch (e.g. `MECH-A`): the script exits with code 2 and lists the valid batches.
  Show that list. Do not guess the closest batch.
- A course that is not in the CSV (e.g. "Quantum Computing lab"): say it is not in the timetable.
  Do not create rows, times or rooms for it. This is the main fabrication risk for this Skill.

## Labs vs lectures
- `CS303` and `CS303L` are different rows. "When is DBMS?" should list both the lecture and the lab
  rows, labelled by `session_type`.

## "Next class" / free-slot questions
- Sort the batch's rows for that day by `start`. A free slot is any gap between one row's `end`
  and the next row's `start`. Report gaps only within 09:00–17:00.

## Conflicting or duplicated rows
- If two rows for the same batch overlap in time, report both and flag the clash. Do not pick one.
