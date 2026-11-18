---
description: Show one batch's classes for one day, using the timetable-helper Skill
argument-hint: <batch> <day>
---

Use the `timetable-helper` Skill to answer this timetable request: $ARGUMENTS

- Expect a batch (for example `CSE-A`) and a weekday. If either is missing, ask for it instead of guessing.
- Run the Skill's lookup script and show the result as a table with Time, Course, Room and Faculty columns.
- If no rows come back, say there are no classes for that batch and day. Do not invent any.
