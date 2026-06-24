import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from pawpal_system import Owner, Pet, Task, Scheduler


def run_demo():
    owner = Owner(name="Jordan")

    # Create two pets
    pet1 = Pet(name="Mochi", species="dog", owner=owner)
    pet2 = Pet(name="Biscuit", species="cat", owner=owner)

    # Tasks for Mochi
    tasks_mochi = [
        Task(title="Morning walk", duration_minutes=30, priority="high"),
        Task(title="Feeding", duration_minutes=10, priority="high"),
        Task(title="Refill water", duration_minutes=5, priority="low"),
    ]

    # Tasks for Biscuit
    tasks_biscuit = [
        Task(title="Playtime", duration_minutes=25, priority="medium"),
        Task(title="Grooming", duration_minutes=40, priority="medium"),
        Task(title="Medication", duration_minutes=5, priority="high"),
    ]

    scheduler = Scheduler(available_minutes=120)

    print("Today's Schedule\n==================\n")

    for pet, tasks in ((pet1, tasks_mochi), (pet2, tasks_biscuit)):
        schedule = scheduler.build_schedule(owner=owner, pet=pet, tasks=tasks)
        print(f"{pet.name} ({pet.species}) - Owner: {owner.name}")
        if schedule.entries:
            for entry in schedule.entries:
                print(f"  {entry.start_time} - {entry.end_time}: {entry.task.title} ({entry.task.duration_minutes} min) [priority: {entry.task.priority}]")
        else:
            print("  No tasks scheduled.")

        if schedule.skipped_tasks:
            print("  Skipped tasks:")
            for t in schedule.skipped_tasks:
                print(f"   - {t.title} ({t.duration_minutes} min) [priority: {t.priority}]")

        print("\n  Reasoning:")
        for line in schedule.explanation.split("\n"):
            print(f"   {line}")

        print("\n")


if __name__ == "__main__":
    run_demo()
