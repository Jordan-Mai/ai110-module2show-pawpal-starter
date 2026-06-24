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
