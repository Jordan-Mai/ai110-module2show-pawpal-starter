# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

Today's Schedule
==================

Mochi (dog) - Owner: Jordan
  08:00 - 08:10: Feeding (10 min) [priority: high]
  08:10 - 08:40: Morning walk (30 min) [priority: high]
  08:40 - 08:45: Refill water (5 min) [priority: low]

  Reasoning:
   Daily plan starts at 08:00 for 3 task(s).
   Available day length: 120 minutes.
   Scheduled 3 task(s): Feeding, Morning walk, Refill water.


Biscuit (cat) - Owner: Jordan
  08:00 - 08:05: Medication (5 min) [priority: high]
  08:05 - 08:30: Playtime (25 min) [priority: medium]
  08:30 - 09:10: Grooming (40 min) [priority: medium]

  Reasoning:
   Daily plan starts at 08:00 for 3 task(s).
   Available day length: 120 minutes.
   Scheduled 3 task(s): Medication, Playtime, Grooming.

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

(.venv) PS C:\Users\mylev\OneDrive\Desktop\PawPal\ai110-module2show-pawpal-starter> pytest
================================================================== test session starts ===================================================================
platform win32 -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\mylev\OneDrive\Desktop\PawPal\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 4 items                                                                                                                                         

tests\test_pawpal.py ..                                                                                                                             [ 50%]
tests\test_tasks.py ..                                                                                                                              [100%]

=================================================================== 4 passed in 0.07s ====================================================================

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

Sorting behavior: Scheduler.sort_by_time(tasks) sorts tasks by a time-like attribute (time, start_time, scheduled_time, scheduled_at) and places unscheduled tasks afterward.

Filtering behavior: Scheduler.filter_tasks(tasks, completed=None, pet_name=None) filters by completion status and/or pet_name.

Conflict detection logic: Scheduler.detect_conflicts(tasks) scans tasks for same-time entries and returns warning strings instead of raising an error.

Recurring task logic: Task.mark_complete() marks a task complete and, when recurrence is daily or weekly, returns a new next-occurrence Task instance.

# Testing PawPal+

Command: python -m pytest tests/test_pawpal.py -q

The current tests cover:
- Task ordering by priority and duration in the generated schedule
- Skipping tasks when the available day time runs out
- Chronological sorting by task time via Scheduler.sort_by_time()
- Daily recurrence behavior in Task.mark_complete()
- Lightweight conflict detection for duplicate scheduled times via Scheduler.detect_conflicts()

Output:
(.venv) PS C:\Users\mylev\OneDrive\Desktop\PawPal\ai110-module2show-pawpal-starter> python -m pytest tests/test_pawpal.py -q
.....                                                                                                                                               [100%]
5 passed in 0.04s

Confidence Level: 5

# Features List
Priority-Based Scheduling — Tasks are ordered by priority (high → medium → low), then by duration, ensuring the most important tasks are scheduled first.

Time-Constrained Planning — The scheduler respects a configurable daily time budget and skips tasks that don't fit, with reasoning provided for each skipped task.

Chronological Sorting — Scheduler.sort_by_time() sorts tasks by their scheduled time attribute (HH:MM format, datetime, or timedelta), placing unscheduled tasks afterward.

Conflict Detection — Scheduler.detect_conflicts() identifies same-time task overlaps and returns non-fatal warning messages instead of crashing, allowing users to be aware of scheduling conflicts.

Task Filtering — Scheduler.filter_tasks() filters tasks by completion status and/or pet name, enabling flexible task queries for reporting and planning.

Daily/Weekly Recurrence — Task.mark_complete() automatically creates a new next-occurrence task for recurring tasks (daily/weekly), with the due date automatically advanced by 1 or 7 days.

Pet Task Management — Pet.add_task() attaches tasks to specific pets and records the pet name on each task for easy filtering and multi-pet scheduling.

Schedule Explanation — Every generated schedule includes a human-readable explanation of why tasks were chosen, skipped, or ordered in a particular way.

Professional UI — Streamlit components (st.dataframe, st.success, st.warning) display sorted tasks, scheduled plans, and conflicts in an intuitive tabular format.

Comprehensive Testing — Full test coverage for scheduling logic, sorting correctness, recurrence behavior, and conflict detection.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Enter Owner & Pet Info: Start by typing an owner nameand a pet name, then select the pet species from the dropdown. This info persists across the session in `st.session_state`.
2. Add Tasks with Priority & Duration: Enter a task title (e.g., "Morning walk"), set the duration in minutes (e.g., 30), and choose a priority level (low/medium/high). Click "Add task" to attach it to the pet.
3. View Sorted Task List: The app displays all tasks in a professional dataframe, automatically sorted by time (if set). Columns show title, duration, priority, time, and recurrence status. You can add multiple tasks and see them organized chronologically.
4. Generate a Daily Schedule: Click "Generate schedule" to run the scheduling algorithm. The scheduler respects a configurable daily time budget (default: 480 minutes/8 hours) and orders tasks by priority.
5. Review Conflict Warnings:If any tasks are scheduled at the same time, a warning banner appears listing the conflicts. This helps you catch overlapping appointments early without crashing the app.
6. View Planned Schedule: A success badge shows how many tasks fit in the day. The planned tasks appear in a sortable dataframe with start time, title, duration, priority, and pet name.
7. See Skipped Tasks: Tasks that don't fit are displayed in a separate warning section, sorted by priority. This helps you understand what couldn't be scheduled and why.
8. Read Schedule Reasoning: The app provides a human-readable explanation of the plan, including the start time, available minutes, which tasks were scheduled, and which were skipped.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
