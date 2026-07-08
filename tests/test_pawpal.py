from datetime import date as Date, time as Time, timedelta
from pawpal_system import Pet, Task, Priority, Frequency, Scheduler, Owner


TARGET = Date(2026, 7, 10)


def make_owner_with_pet():
    owner = Owner(name="Alice")
    pet = Pet(name="Buddy", species="Dog")
    owner.add_pet(pet)
    return owner, pet


# ============================================================================
# Original Tests
# ============================================================================

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


# ============================================================================
# Group 1: Sorting Correctness
# ============================================================================

def test_sort_by_time_ascending():
    task1 = Task(title="A", time=Time(10, 0), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task2 = Task(title="B", time=Time(8, 0), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task3 = Task(title="C", time=Time(9, 30), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)

    sorted_tasks = Scheduler.sort_by_time([task1, task2, task3])
    assert [t.title for t in sorted_tasks] == ["B", "C", "A"]


def test_sort_by_time_none_times_sort_last():
    task1 = Task(title="A", time=Time(10, 0), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task2 = Task(title="B", time=None, duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task3 = Task(title="C", time=Time(8, 0), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)

    sorted_tasks = Scheduler.sort_by_time([task1, task2, task3])
    assert sorted_tasks[-1].title == "B"
    assert [t.title for t in sorted_tasks[:2]] == ["C", "A"]


def test_sort_by_date_ascending():
    task1 = Task(title="A", date=Date(2026, 7, 15), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task2 = Task(title="B", date=Date(2026, 7, 10), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task3 = Task(title="C", date=Date(2026, 7, 12), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)

    sorted_tasks = Scheduler.sort_by_date([task1, task2, task3])
    assert [t.title for t in sorted_tasks] == ["B", "C", "A"]


def test_sort_by_date_none_dates_sort_last():
    task1 = Task(title="A", date=Date(2026, 7, 15), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task2 = Task(title="B", date=None, duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task3 = Task(title="C", date=Date(2026, 7, 10), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)

    sorted_tasks = Scheduler.sort_by_date([task1, task2, task3])
    assert sorted_tasks[-1].title == "B"
    assert [t.title for t in sorted_tasks[:2]] == ["C", "A"]


def test_sort_by_priority_descending():
    task1 = Task(title="A", duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task2 = Task(title="B", duration=30, priority=Priority.VERY_HIGH, frequency=Frequency.DAILY)
    task3 = Task(title="C", duration=30, priority=Priority.VERY_LOW, frequency=Frequency.DAILY)

    sorted_tasks = Scheduler.sort_by_priority([task1, task2, task3])
    assert [t.title for t in sorted_tasks] == ["B", "A", "C"]


def test_sort_by_time_with_priority_tie_break():
    task1 = Task(title="A", time=Time(10, 0), duration=30, priority=Priority.LOW, frequency=Frequency.DAILY)
    task2 = Task(title="B", time=Time(10, 0), duration=30, priority=Priority.VERY_HIGH, frequency=Frequency.DAILY)
    task3 = Task(title="C", time=Time(9, 0), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)

    sorted_tasks = Scheduler.sort_by_time_with_priority([task1, task2, task3])
    assert [t.title for t in sorted_tasks] == ["C", "B", "A"]


def test_sort_by_priority_with_time_tie_break():
    task1 = Task(title="A", time=Time(10, 0), duration=30, priority=Priority.HIGH, frequency=Frequency.DAILY)
    task2 = Task(title="B", time=Time(8, 0), duration=30, priority=Priority.HIGH, frequency=Frequency.DAILY)
    task3 = Task(title="C", time=Time(9, 0), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)

    sorted_tasks = Scheduler.sort_by_priority_with_time([task1, task2, task3])
    assert sorted_tasks[0].title == "B"
    assert sorted_tasks[1].title == "A"
    assert sorted_tasks[2].title == "C"


def test_sort_does_not_mutate_original_list():
    task1 = Task(title="A", time=Time(10, 0), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task2 = Task(title="B", time=Time(8, 0), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    original = [task1, task2]
    original_titles = [t.title for t in original]

    Scheduler.sort_by_time(original)

    assert [t.title for t in original] == original_titles


# ============================================================================
# Group 2: Recurrence Logic
# ============================================================================

def test_daily_task_mark_complete_creates_next_day_task():
    owner, pet = make_owner_with_pet()
    task = pet.add_task(
        title="Feed",
        date=TARGET,
        time=Time(8, 0),
        duration=15,
        priority=Priority.HIGH,
        frequency=Frequency.DAILY
    )
    assert len(pet.tasks) == 1

    task.mark_complete()

    assert len(pet.tasks) == 2
    new_task = pet.tasks[1]
    assert new_task.title == "Feed"
    assert new_task.date == TARGET + timedelta(days=1)
    assert new_task.time == Time(8, 0)
    assert new_task.completed is False


def test_weekly_task_mark_complete_creates_next_week_task():
    owner, pet = make_owner_with_pet()
    task = pet.add_task(
        title="Vet Check",
        date=TARGET,
        time=Time(10, 0),
        duration=60,
        priority=Priority.MEDIUM,
        frequency=Frequency.WEEKLY
    )

    task.mark_complete()

    assert len(pet.tasks) == 2
    new_task = pet.tasks[1]
    assert new_task.title == "Vet Check"
    assert new_task.date == TARGET + timedelta(days=7)
    assert new_task.frequency == Frequency.WEEKLY


def test_one_time_task_mark_complete_no_new_task():
    owner, pet = make_owner_with_pet()
    task = pet.add_task(
        title="One-time Event",
        date=TARGET,
        time=Time(14, 0),
        duration=45,
        priority=Priority.MEDIUM,
        frequency=Frequency.ONE_TIME
    )

    task.mark_complete()

    assert len(pet.tasks) == 1
    assert pet.tasks[0].completed is True


def test_mark_complete_without_pet_no_error():
    task = Task(
        title="Feed",
        date=TARGET,
        time=Time(8, 0),
        duration=15,
        priority=Priority.HIGH,
        frequency=Frequency.DAILY
    )

    task.mark_complete()

    assert task.completed is True


def test_recurring_task_inherits_attributes():
    owner, pet = make_owner_with_pet()
    task = pet.add_task(
        title="Walk",
        date=TARGET,
        time=Time(9, 0),
        duration=45,
        priority=Priority.VERY_HIGH,
        frequency=Frequency.DAILY
    )

    task.mark_complete()

    new_task = pet.tasks[1]
    assert new_task.title == "Walk"
    assert new_task.time == Time(9, 0)
    assert new_task.duration == 45
    assert new_task.priority == Priority.VERY_HIGH
    assert new_task.frequency == Frequency.DAILY


# ============================================================================
# Group 3: Filter Methods
# ============================================================================

def test_filter_by_completed_true():
    task1 = Task(title="A", completed=True, duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task2 = Task(title="B", completed=False, duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task3 = Task(title="C", completed=True, duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)

    filtered = Scheduler.filter_by_completed([task1, task2, task3], completed=True)

    assert len(filtered) == 2
    assert [t.title for t in filtered] == ["A", "C"]


def test_filter_by_completed_false():
    task1 = Task(title="A", completed=True, duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task2 = Task(title="B", completed=False, duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task3 = Task(title="C", completed=False, duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)

    filtered = Scheduler.filter_by_completed([task1, task2, task3], completed=False)

    assert len(filtered) == 2
    assert [t.title for t in filtered] == ["B", "C"]


def test_filter_by_date_matching():
    task1 = Task(title="A", date=TARGET, duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task2 = Task(title="B", date=Date(2026, 7, 11), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task3 = Task(title="C", date=TARGET, duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)

    filtered = Scheduler.filter_by_date([task1, task2, task3], TARGET)

    assert len(filtered) == 2
    assert [t.title for t in filtered] == ["A", "C"]


def test_filter_by_date_no_match_returns_empty():
    task1 = Task(title="A", date=TARGET, duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task2 = Task(title="B", date=Date(2026, 7, 11), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)

    filtered = Scheduler.filter_by_date([task1, task2], Date(2026, 8, 1))

    assert filtered == []


def test_filter_by_pet_name_matching():
    buddy = Pet(name="Buddy", species="Dog")
    max_pet = Pet(name="Max", species="Cat")

    task1 = Task(title="A", duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY, pet=buddy)
    task2 = Task(title="B", duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY, pet=max_pet)
    task3 = Task(title="C", duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY, pet=buddy)

    filtered = Scheduler.filter_by_pet([task1, task2, task3], "Buddy")

    assert len(filtered) == 2
    assert [t.title for t in filtered] == ["A", "C"]


def test_filter_by_pet_name_no_match_returns_empty():
    buddy = Pet(name="Buddy", species="Dog")
    task1 = Task(title="A", duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY, pet=buddy)

    filtered = Scheduler.filter_by_pet([task1], "Unknown")

    assert filtered == []


# ============================================================================
# Group 4: Conflict Detection
# ============================================================================

def test_exact_same_start_time_conflict():
    owner, pet = make_owner_with_pet()
    task1 = pet.add_task(
        title="Feed",
        date=TARGET,
        time=Time(8, 0),
        duration=30,
        priority=Priority.VERY_HIGH,
        frequency=Frequency.DAILY
    )
    task2 = pet.add_task(
        title="Walk",
        date=TARGET,
        time=Time(8, 0),
        duration=30,
        priority=Priority.LOW,
        frequency=Frequency.DAILY
    )

    schedule, reasoning = owner.scheduler.generate_schedule(owner, date=TARGET)

    assert len(schedule) == 1
    assert schedule[0].title == "Feed"
    assert any("conflict" in reason.lower() for reason in reasoning)


def test_adjacent_tasks_no_conflict():
    owner, pet = make_owner_with_pet()
    task1 = pet.add_task(
        title="Task A",
        date=TARGET,
        time=Time(8, 0),
        duration=60,
        priority=Priority.MEDIUM,
        frequency=Frequency.DAILY
    )
    task2 = pet.add_task(
        title="Task B",
        date=TARGET,
        time=Time(9, 0),
        duration=60,
        priority=Priority.MEDIUM,
        frequency=Frequency.DAILY
    )

    schedule, reasoning = owner.scheduler.generate_schedule(owner, date=TARGET)

    assert len(schedule) == 2
    assert [t.title for t in schedule] == ["Task A", "Task B"]


def test_partial_overlap_conflict():
    owner, pet = make_owner_with_pet()
    task1 = pet.add_task(
        title="Task A",
        date=TARGET,
        time=Time(8, 0),
        duration=60,
        priority=Priority.HIGH,
        frequency=Frequency.DAILY
    )
    task2 = pet.add_task(
        title="Task B",
        date=TARGET,
        time=Time(8, 30),
        duration=60,
        priority=Priority.MEDIUM,
        frequency=Frequency.DAILY
    )

    schedule, reasoning = owner.scheduler.generate_schedule(owner, date=TARGET)

    assert len(schedule) == 1
    assert schedule[0].title == "Task A"


def test_none_time_task_always_added():
    owner, pet = make_owner_with_pet()
    task1 = pet.add_task(
        title="Timed Task",
        date=TARGET,
        time=Time(8, 0),
        duration=120,
        priority=Priority.MEDIUM,
        frequency=Frequency.DAILY
    )
    task2 = pet.add_task(
        title="No Time Task",
        date=TARGET,
        time=None,
        duration=30,
        priority=Priority.LOW,
        frequency=Frequency.DAILY
    )

    schedule, reasoning = owner.scheduler.generate_schedule(owner, date=TARGET)

    assert len(schedule) == 2
    assert any(t.title == "No Time Task" for t in schedule)


def test_higher_priority_wins_conflict():
    owner, pet = make_owner_with_pet()
    task1 = pet.add_task(
        title="Low Priority",
        date=TARGET,
        time=Time(8, 0),
        duration=30,
        priority=Priority.LOW,
        frequency=Frequency.DAILY
    )
    task2 = pet.add_task(
        title="High Priority",
        date=TARGET,
        time=Time(8, 0),
        duration=30,
        priority=Priority.VERY_HIGH,
        frequency=Frequency.DAILY
    )

    schedule, reasoning = owner.scheduler.generate_schedule(owner, date=TARGET)

    assert len(schedule) == 1
    assert schedule[0].title == "High Priority"


def test_non_overlapping_tasks_both_scheduled():
    owner, pet = make_owner_with_pet()
    task1 = pet.add_task(
        title="Morning Task",
        date=TARGET,
        time=Time(8, 0),
        duration=60,
        priority=Priority.MEDIUM,
        frequency=Frequency.DAILY
    )
    task2 = pet.add_task(
        title="Afternoon Task",
        date=TARGET,
        time=Time(14, 0),
        duration=60,
        priority=Priority.MEDIUM,
        frequency=Frequency.DAILY
    )

    schedule, reasoning = owner.scheduler.generate_schedule(owner, date=TARGET)

    assert len(schedule) == 2


# ============================================================================
# Group 5: Generate Schedule Pipeline
# ============================================================================

def test_generate_schedule_excludes_completed_tasks():
    owner, pet = make_owner_with_pet()
    task1 = pet.add_task(
        title="Complete",
        date=TARGET,
        time=Time(8, 0),
        duration=30,
        priority=Priority.MEDIUM,
        frequency=Frequency.DAILY
    )
    task2 = pet.add_task(
        title="Incomplete",
        date=TARGET,
        time=Time(9, 0),
        duration=30,
        priority=Priority.MEDIUM,
        frequency=Frequency.DAILY
    )

    task1.completed = True
    schedule, reasoning = owner.scheduler.generate_schedule(owner, date=TARGET)

    assert len(schedule) == 1
    assert schedule[0].title == "Incomplete"


def test_generate_schedule_only_includes_target_date():
    owner, pet = make_owner_with_pet()
    task1 = pet.add_task(
        title="Target Date",
        date=TARGET,
        time=Time(8, 0),
        duration=30,
        priority=Priority.MEDIUM,
        frequency=Frequency.DAILY
    )
    task2 = pet.add_task(
        title="Other Date",
        date=Date(2026, 7, 11),
        time=Time(8, 0),
        duration=30,
        priority=Priority.MEDIUM,
        frequency=Frequency.DAILY
    )

    schedule, reasoning = owner.scheduler.generate_schedule(owner, date=TARGET)

    assert len(schedule) == 1
    assert schedule[0].title == "Target Date"


def test_generate_schedule_sorted_priority_then_time():
    owner, pet = make_owner_with_pet()
    task1 = pet.add_task(
        title="Low Priority Late",
        date=TARGET,
        time=Time(14, 0),
        duration=30,
        priority=Priority.LOW,
        frequency=Frequency.DAILY
    )
    task2 = pet.add_task(
        title="High Priority Early",
        date=TARGET,
        time=Time(8, 0),
        duration=30,
        priority=Priority.VERY_HIGH,
        frequency=Frequency.DAILY
    )
    task3 = pet.add_task(
        title="High Priority Late",
        date=TARGET,
        time=Time(14, 0),
        duration=30,
        priority=Priority.VERY_HIGH,
        frequency=Frequency.DAILY
    )

    schedule, reasoning = owner.scheduler.generate_schedule(owner, date=TARGET)

    assert schedule[0].title == "High Priority Early"
    assert schedule[1].title == "High Priority Late" or schedule[1].title == "Low Priority Late"


def test_generate_schedule_returns_reasoning_entries():
    owner, pet = make_owner_with_pet()
    task1 = pet.add_task(
        title="Task 1",
        date=TARGET,
        time=Time(8, 0),
        duration=30,
        priority=Priority.MEDIUM,
        frequency=Frequency.DAILY
    )
    task2 = pet.add_task(
        title="Task 2",
        date=TARGET,
        time=Time(9, 0),
        duration=30,
        priority=Priority.MEDIUM,
        frequency=Frequency.DAILY
    )

    schedule, reasoning = owner.scheduler.generate_schedule(owner, date=TARGET)

    assert len(reasoning) >= 2
    assert all(isinstance(r, str) for r in reasoning)


def test_generate_schedule_default_date_is_tomorrow():
    owner, pet = make_owner_with_pet()
    tomorrow = Date.today() + timedelta(days=1)

    task1 = pet.add_task(
        title="Tomorrow Task",
        date=tomorrow,
        time=Time(8, 0),
        duration=30,
        priority=Priority.MEDIUM,
        frequency=Frequency.DAILY
    )
    task2 = pet.add_task(
        title="Today Task",
        date=Date.today(),
        time=Time(8, 0),
        duration=30,
        priority=Priority.MEDIUM,
        frequency=Frequency.DAILY
    )

    schedule, reasoning = owner.scheduler.generate_schedule(owner)

    assert len(schedule) == 1
    assert schedule[0].title == "Tomorrow Task"


# ============================================================================
# Group 6: Owner / Pet CRUD
# ============================================================================

def test_owner_add_pet():
    owner = Owner(name="Alice")
    pet = Pet(name="Buddy", species="Dog")

    owner.add_pet(pet)

    assert pet in owner.pets
    assert len(owner.pets) == 1


def test_owner_remove_pet():
    owner = Owner(name="Alice")
    pet = Pet(name="Buddy", species="Dog")
    owner.add_pet(pet)

    owner.remove_pet(pet)

    assert pet not in owner.pets
    assert len(owner.pets) == 0


def test_owner_find_pet_found():
    owner = Owner(name="Alice")
    pet = Pet(name="Buddy", species="Dog")
    owner.add_pet(pet)

    found = owner.find_pet("Buddy")

    assert found is pet


def test_owner_find_pet_not_found():
    owner = Owner(name="Alice")
    pet = Pet(name="Buddy", species="Dog")
    owner.add_pet(pet)

    found = owner.find_pet("Max")

    assert found is None


def test_owner_find_task_across_pets():
    owner = Owner(name="Alice")
    pet1 = Pet(name="Buddy", species="Dog")
    pet2 = Pet(name="Max", species="Cat")
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = pet1.add_task(title="Walk", date=TARGET, time=Time(8, 0), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task2 = pet2.add_task(title="Feed", date=TARGET, time=Time(9, 0), duration=15, priority=Priority.MEDIUM, frequency=Frequency.DAILY)

    found = owner.find_task("Feed")

    assert found is task2


def test_owner_find_task_not_found_returns_none():
    owner = Owner(name="Alice")
    pet = Pet(name="Buddy", species="Dog")
    owner.add_pet(pet)
    pet.add_task(title="Walk", date=TARGET, time=Time(8, 0), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)

    found = owner.find_task("Nonexistent")

    assert found is None


def test_owner_get_all_tasks_flattens_pets():
    owner = Owner(name="Alice")
    pet1 = Pet(name="Buddy", species="Dog")
    pet2 = Pet(name="Max", species="Cat")
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = pet1.add_task(title="Walk", date=TARGET, time=Time(8, 0), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task2 = pet1.add_task(title="Play", date=TARGET, time=Time(10, 0), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)
    task3 = pet2.add_task(title="Feed", date=TARGET, time=Time(9, 0), duration=15, priority=Priority.MEDIUM, frequency=Frequency.DAILY)

    all_tasks = owner.get_all_tasks()

    assert len(all_tasks) == 3
    assert task1 in all_tasks
    assert task2 in all_tasks
    assert task3 in all_tasks


def test_pet_remove_task_removes_from_list():
    pet = Pet(name="Buddy", species="Dog")
    task = pet.add_task(title="Walk", date=TARGET, time=Time(8, 0), duration=30, priority=Priority.MEDIUM, frequency=Frequency.DAILY)

    pet.remove_task(task)

    assert task not in pet.tasks
    assert len(pet.tasks) == 0


# ============================================================================
# Group 7: Full Integration Flow
# ============================================================================

def test_full_flow_owner_pet_task_to_schedule():
    owner = Owner(name="Alice")
    pet = Pet(name="Buddy", species="Dog")
    owner.add_pet(pet)

    task = pet.add_task(
        title="Morning Walk",
        date=TARGET,
        time=Time(8, 0),
        duration=30,
        priority=Priority.HIGH,
        frequency=Frequency.DAILY
    )

    owner.scheduler.generate_schedule(owner, date=TARGET)

    schedule, reasoning = owner.scheduler.generate_schedule(owner, date=TARGET)

    assert len(schedule) == 1
    assert schedule[0].title == "Morning Walk"
    assert len(reasoning) >= 1


def test_full_flow_multiple_pets_conflict_resolution():
    owner = Owner(name="Alice")
    pet1 = Pet(name="Buddy", species="Dog")
    pet2 = Pet(name="Max", species="Cat")
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = pet1.add_task(
        title="Dog Walk",
        date=TARGET,
        time=Time(8, 0),
        duration=30,
        priority=Priority.VERY_HIGH,
        frequency=Frequency.DAILY
    )
    task2 = pet2.add_task(
        title="Cat Feed",
        date=TARGET,
        time=Time(8, 0),
        duration=15,
        priority=Priority.LOW,
        frequency=Frequency.DAILY
    )

    schedule, reasoning = owner.scheduler.generate_schedule(owner, date=TARGET)

    assert len(schedule) == 1
    assert schedule[0].title == "Dog Walk"


def test_full_flow_complete_and_reschedule():
    owner = Owner(name="Alice")
    pet = Pet(name="Buddy", species="Dog")
    owner.add_pet(pet)

    today = Date.today()
    tomorrow = today + timedelta(days=1)

    task = pet.add_task(
        title="Daily Feed",
        date=today,
        time=Time(8, 0),
        duration=15,
        priority=Priority.HIGH,
        frequency=Frequency.DAILY
    )

    task.mark_complete()

    assert len(pet.tasks) == 2
    new_task = pet.tasks[1]
    assert new_task.date == tomorrow
    assert new_task.completed is False

    schedule, reasoning = owner.scheduler.generate_schedule(owner, date=tomorrow)

    assert len(schedule) == 1
    assert schedule[0].title == "Daily Feed"
