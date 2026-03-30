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

## Smarter Scheduling

PawPal+ now includes smarter scheduling features to make daily planning more useful:

- **Time & Priority Sorting** – Tasks are ordered by start time, then by priority, so the most important tasks at each time slot appear first.
- **Pet Filtering** – View schedules for all pets together or filter down to a single pet in the UI.
- **Recurring Tasks** – Daily and weekly tasks automatically generate a new instance for the next occurrence when marked complete.
- **Conflict Detection** – Lightweight conflict checks warn when two tasks overlap in time (for the same or different pets), without stopping the app.
- **Task Filtering** – Tasks can be filtered by completion status or by pet name in the scheduler logic, enabling focused views and reports.

## Testing PawPal+

To run the automated test suite, use:

```bash
python -m pytest
```

The current tests cover:
* Core `Task` behavior (creation and completion).
* Adding tasks to a `Pet`.
* Scheduler sorting logic to ensure tasks are ordered chronologically and by priority.
* Recurring task handling for daily tasks (creating the next day’s task on completion).
* Conflict detection for overlapping tasks.

**Confidence Level:** ⭐⭐⭐☆☆ (3/5)

The suite validates key happy paths and several edge cases, but broader coverage (e.g., weekly recurrences, filtering combinations, and more complex schedules) would be needed for higher confidence.