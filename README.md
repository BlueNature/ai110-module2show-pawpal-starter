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

**Example CLI output:** (Streamlit output is formatted cleanly as a table)
```
Tomorrow's Generated Schedule
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Task(title='Vet visit', date=datetime.date(2026, 7, 7), time=datetime.time(10, 30), duration=200, priority=<Priority.VERY_HIGH: 5>, frequency=<Frequency.ONE_TIME: 'one-time'>, completed=False)
Task(title='walkies!', date=datetime.date(2026, 7, 7), time=datetime.time(8, 0), duration=60, priority=<Priority.HIGH: 4>, frequency=<Frequency.DAILY: 'daily'>, completed=False)
Task(title='brushing', date=datetime.date(2026, 7, 7), time=datetime.time(14, 0), duration=15, priority=<Priority.MEDIUM: 3>, frequency=<Frequency.WEEKLY: 'weekly'>, completed=False)
Task(title='??????????', date=datetime.date(2026, 7, 7), time=datetime.time(20, 0), duration=30, priority=<Priority.MEDIUM: 3>, frequency=<Frequency.ONE_TIME: 'one-time'>, completed=False)
Task(title="steal dad's socks", date=datetime.date(2026, 7, 7), time=datetime.time(8, 0), duration=9999, priority=<Priority.LOW: 2>, frequency=<Frequency.DAILY: 'daily'>, completed=False)

Scheduling Reasoning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Added 'Vet visit' for Spot at 10:30:00.
Added 'walkies!' for Dot at 08:00:00.
Skipped 'Bath Time' for Spot — time conflict with 'Vet visit'.
Added 'brushing' for Pip at 14:00:00.
Added '??????????' for Lord Biscuit Mc-Stinkypaws III at 20:00:00.
Added 'steal dad's socks' for Lord Biscuit Mc-Stinkypaws III at 08:00:00.
Skipped 'Nap (do not disturb or else)' for Lord Biscuit Mc-Stinkypaws III — time conflict with 'Vet visit'.
```

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

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_by_date, Scheduler.sort_by_time, Scheduler.sort_by_priority | Sorting criteria can include date, time (separate), and priority |
| Task sorting with tiebreakers | Scheduler.sort_by_time_with_priority, Scheduler.sort_by_priority_with_time | More complex sorting: uses one criterion with another to settle tiebreakers |
| Filtering | Scheduler.filter_by_completed, Scheduler.filter_by_date, Scheduler.filter_by_pet | Filtering criteria can include completion status, specific date, and pet |
| Conflict handling | Scheduler.generate_schedule | Checks for overlapping time slots when adding a new task and may skip it accordingly |
| Recurring tasks | Task.mark_complete | If frequency is daily or weekly, automatically populates a new Task with identical attributes and appropriate time |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
