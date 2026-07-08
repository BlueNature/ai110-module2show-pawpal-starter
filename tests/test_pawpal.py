from pawpal_system import Pet, Task, Priority, Frequency, Scheduler, Owner


def test_mark_complete_changes_status():
    task = Task(title="Feed", duration=5, priority=Priority.HIGH, frequency=Frequency.DAILY)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog")
    assert len(pet.tasks) == 0
    pet.add_task(title="Walk", duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    assert len(pet.tasks) == 1
