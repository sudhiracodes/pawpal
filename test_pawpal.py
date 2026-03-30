from datetime import datetime
from pawpal_system import Task, Pet

def test_task_completion():
    """Verify that calling mark_complete() actually changes the task's status."""
    # Create a task using your advanced parameters (duration, priority)
    task = Task("Morning Walk", datetime.now(), "Daily", 30, 5)
    
    # It should start as incomplete
    assert not task.is_complete()
    
    # Mark it complete
    task.mark_complete()
    
    # It should now be complete
    assert task.is_complete()

def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    # Create a pet
    pet = Pet("Fido", "Dog")
    
    # It should start with 0 tasks
    assert len(pet.get_tasks()) == 0
    
    # Add a task
    new_task = Task("Morning Walk", datetime.now(), "Daily", 30, 5)
    pet.add_task(new_task)
    
    # It should now have 1 task
    assert len(pet.get_tasks()) == 1