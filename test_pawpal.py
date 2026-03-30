from datetime import datetime, date, timedelta
from pawpal_system import Owner, Task, Pet, Scheduler

def test_task_completion():
    """Verify that calling mark_complete() actually changes the task's status."""
    task = Task("Morning Walk", datetime.now(), "Daily", 30, 5)
    assert not task.is_complete()
    task.mark_complete()
    assert task.is_complete()

def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet("Fido", "Dog")
    assert len(pet.get_tasks()) == 0
    new_task = Task("Morning Walk", datetime.now(), "Daily", 30, 5)
    pet.add_task(new_task)
    assert len(pet.get_tasks()) == 1

def test_scheduler_sorts_tasks_chronologically():
    """Sorting Correctness: Verify tasks are sorted by time correctly."""
    owner = Owner("Alex")
    scheduler = Scheduler(owner)
    pet = Pet("Fido", "Dog")
    owner.add_pet(pet)
    now = datetime.now()

    # Create tasks out of order
    t1 = Task("Lunch", now + timedelta(hours=2), "Once", 15, 2)
    t2 = Task("Breakfast", now, "Once", 30, 3)
    t3 = Task("Dinner", now + timedelta(hours=4), "Once", 45, 1)

    pet.add_task(t1)
    pet.add_task(t2)
    pet.add_task(t3)

    # Use your custom sorting method
    sorted_tasks = scheduler.sort_by_time_and_priority(owner.get_all_tasks())

    # Breakfast should be sorted to the very front
    assert sorted_tasks[0].description() == "Breakfast"
    assert sorted_tasks[-1].description() == "Dinner"

def test_daily_task_recurrence_creates_next_day_task():
    """Recurrence Logic: marking a daily task complete should create a new task for the following day."""
    owner = Owner("Alex")
    scheduler = Scheduler(owner)
    pet = Pet("Fido", "Dog")
    owner.add_pet(pet)
    
    start_time = datetime(2024, 1, 1, 8, 0)
    daily_task = Task("Daily Walk", start_time, "Daily", 30, 5)
    pet.add_task(daily_task)

    # Use your system's mark_task_complete method
    new_task = scheduler.mark_task_complete(daily_task)

    # Original task should be complete
    assert daily_task.is_complete()

    # A new task should exist for the next day, same time
    assert new_task is not None
    assert new_task.time() == start_time + timedelta(days=1)
    
    # Verify the new task was actually attached to the pet
    assert new_task in pet.get_tasks()

def test_scheduler_detects_conflicting_tasks():
    """Conflict Detection: Verify that the Scheduler flags overlapping times."""
    owner = Owner("Alex")
    scheduler = Scheduler(owner)
    pet = Pet("Fido", "Dog")
    owner.add_pet(pet)
    
    start_time = datetime(2024, 1, 1, 9, 0)

    # Task 1 starts at 9:00 and lasts 30 mins (ends 9:30)
    task1 = Task("Morning Walk", start_time, "Once", 30, 3)
    
    # Task 2 starts at 9:15, which overlaps with Task 1!
    task2 = Task("Vet Visit", start_time + timedelta(minutes=15), "Once", 60, 5)

    pet.add_task(task1)
    pet.add_task(task2)

    # Pass the tasks to your conflict checker
    conflicts = scheduler.check_conflicts(owner.get_all_tasks())

    # It should flag both tasks as being in conflict
    assert len(conflicts) == 2
    assert task1 in conflicts
    assert task2 in conflicts