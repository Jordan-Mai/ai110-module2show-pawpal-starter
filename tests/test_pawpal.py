from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def test_scheduler_orders_by_priority_then_duration():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", owner=owner)

    tasks = [
        Task(title="Grooming", duration_minutes=30, priority="medium"),
        Task(title="Morning walk", duration_minutes=20, priority="high"),
        Task(title="Playtime", duration_minutes=15, priority="high"),
        Task(title="Refill water", duration_minutes=5, priority="low"),
    ]

    schedule = Scheduler(available_minutes=120).build_schedule(owner=owner, pet=pet, tasks=tasks)

    assert [entry.task.title for entry in schedule.entries] == ["Playtime", "Morning walk", "Grooming", "Refill water"]
    assert schedule.skipped_tasks == []
    assert "Scheduled 4 task(s)" in schedule.explanation


def test_scheduler_skips_tasks_when_time_runs_out():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", owner=owner)

    tasks = [
        Task(title="Morning walk", duration_minutes=60, priority="high"),
        Task(title="Feeding", duration_minutes=15, priority="high"),
        Task(title="Grooming", duration_minutes=90, priority="medium"),
        Task(title="Playtime", duration_minutes=45, priority="medium"),
    ]

    schedule = Scheduler(available_minutes=90).build_schedule(owner=owner, pet=pet, tasks=tasks)

    assert [entry.task.title for entry in schedule.entries] == ["Feeding", "Morning walk"]
    assert [task.title for task in schedule.skipped_tasks] == ["Playtime", "Grooming"]
    assert "Skipped 2 task(s)" in schedule.explanation


def test_sort_by_time_returns_chronological_order():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", owner=owner)
    tasks = [
        Task(title="Midday snack", duration_minutes=10, priority="medium", time="12:00"),
        Task(title="Morning walk", duration_minutes=30, priority="high", time="08:00"),
        Task(title="Evening play", duration_minutes=20, priority="low", time="18:00"),
    ]

    sorted_tasks = Scheduler().sort_by_time(tasks)

    assert [task.title for task in sorted_tasks] == ["Morning walk", "Midday snack", "Evening play"]


def test_daily_task_recurrence_creates_next_day_task():
    task = Task(
        title="Refill water",
        duration_minutes=5,
        priority="low",
        time="08:30",
        recurrence="daily",
        due_date=datetime(2026, 6, 24, 8, 30),
    )

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.recurrence == "daily"
    assert next_task.completed is False
    assert next_task.due_date == datetime(2026, 6, 25, 8, 30)


def test_scheduler_detects_time_conflicts():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", owner=owner)
    tasks = [
        Task(title="Feeding", duration_minutes=10, priority="high", time="08:00", pet_name="Mochi"),
        Task(title="Medication", duration_minutes=5, priority="high", time="08:00", pet_name="Mochi"),
    ]

    warnings = Scheduler().detect_conflicts(tasks)

    assert len(warnings) == 1
    assert "Conflict detected at 08:00" in warnings[0]
    assert "Feeding" in warnings[0] and "Medication" in warnings[0]
