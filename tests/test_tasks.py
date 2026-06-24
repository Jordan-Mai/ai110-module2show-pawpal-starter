from pawpal_system import Owner, Pet, Task


def test_task_completion_marks_completed():
    task = Task(title="Test task", duration_minutes=10, priority="low")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_pet_add_task_increases_count():
    owner = Owner(name="Alex")
    pet = Pet(name="Rex", species="dog", owner=owner)
    assert len(pet.tasks) == 0
    t = Task(title="Walk", duration_minutes=20, priority="high")
    pet.add_task(t)
    assert len(pet.tasks) == 1
    assert pet.tasks[0] is t
