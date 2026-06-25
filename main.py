import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from pawpal_system import Owner, Pet, Task, Scheduler


def run_demo():
    owner = Owner(name="Jordan")

    # Create two pets
    pet1 = Pet(name="Mochi", species="dog", owner=owner)
    pet2 = Pet(name="Biscuit", species="cat", owner=owner)

    # Tasks for Mochi (intentionally out of chronological order)
    tasks_mochi = [
        Task(title="Feeding", duration_minutes=10, priority="high", time="08:00"),
        Task(title="Refill water", duration_minutes=5, priority="low", time="08:30", recurrence="daily"),
        Task(title="Morning walk", duration_minutes=30, priority="high", time="09:00"),
    ]

    # Tasks for Biscuit (out of order, with a same-time conflict at 08:30)
    tasks_biscuit = [
        Task(title="Grooming", duration_minutes=40, priority="medium", time="10:30"),
        Task(title="Playtime", duration_minutes=25, priority="medium", time="09:15"),
        Task(title="Medication", duration_minutes=5, priority="high", time="08:30"),
    ]

    # Attach tasks to their pets (this sets pet_name on each Task)
    for t in tasks_mochi:
        pet1.add_task(t)
    for t in tasks_biscuit:
        pet2.add_task(t)

    scheduler = Scheduler(available_minutes=120)

    print("Combined (unsorted) task list:")
    combined = [pet2.tasks[2], pet1.tasks[0], pet2.tasks[1], pet1.tasks[2], pet1.tasks[1]]
    for t in combined:
        print(f" - {t.title} (pet={t.pet_name}, time={t.time}, dur={t.duration_minutes})")

    print("\nSorted by time:")
    sorted_tasks = scheduler.sort_by_time(combined)
    for t in sorted_tasks:
        print(f" - {t.time} — {t.title} (pet={t.pet_name})")

    print("\nConflict warnings:")
    warnings = scheduler.detect_conflicts(combined)
    if warnings:
        for warning in warnings:
            print(f" - WARNING: {warning}")
    else:
        print(" - No conflicts detected.")

    print("\nFilter: uncompleted tasks for Mochi:")
    uncompleted_mochi = scheduler.filter_tasks(sorted_tasks, completed=False, pet_name="Mochi")
    for t in uncompleted_mochi:
        print(f" - {t.title} (completed={t.completed})")

    # Demonstrate recurrence handling: mark Refill water complete and auto-create next occurrence
    print("\nDemonstrating recurrence handling:")
    refill = next((t for t in pet1.tasks if t.title == "Refill water"), None)
    if refill:
        new_task = refill.mark_complete()
        print(f"Marked '{refill.title}' complete -> new_task returned: {new_task is not None}")
        if new_task:
            pet1.add_task(new_task)
            print(f"New recurring task added for {pet1.name}: {new_task.title} (completed={new_task.completed}, recurrence={new_task.recurrence})")

    print("\nFull Mochi task list after recurrence handling:")
    for t in pet1.tasks:
        print(f" - {t.title} (completed={t.completed}, recurrence={t.recurrence})")


if __name__ == "__main__":
    run_demo()
