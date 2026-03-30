from datetime import datetime, date, time
from pawpal_system import Owner, Pet, Task, Scheduler

def run_demo():
    # 1. Setup Owner and 2 Pets
    owner = Owner("Alex")
    fido = Pet("Fido", "Dog")
    whiskers = Pet("Whiskers", "Cat")
    
    owner.add_pet(fido)
    owner.add_pet(whiskers)

    # 2. Create datetimes for today at different times
    early_morning = datetime.combine(date.today(), time(7, 30))
    morning = datetime.combine(date.today(), time(8, 0))
    afternoon = datetime.combine(date.today(), time(14, 0))

    # 3. Add Tasks to specific pets
    # Whiskers' Tasks:
    whiskers.add_task(Task("Feed Breakfast", early_morning, "Daily", 10, 5))
    whiskers.add_task(Task("Brush Fur", afternoon, "Weekly", 15, 3))
    
    # Fido's Tasks:
    fido.add_task(Task("Morning Walk", morning, "Daily", 30, 4))
    fido.add_task(Task("Vet Visit", afternoon, "Once", 60, 5))

    # 4. Schedule and Print
    scheduler = Scheduler(owner)
    
    print("\n🐾 PAWPAL+ TODAY'S SCHEDULE 🐾")
    print("-" * 60)
    
    schedule = scheduler.get_today_schedule(date.today())
    
    for task in schedule:
        # Quick loop to find which pet owns this specific task
        pet_name = "Unknown"
        for pet in owner.pets():
            if task in pet.get_tasks():
                pet_name = pet.name()
                break
                
        t_time = task.time().strftime('%H:%M')
        # Now it prints the pet's name right before the task!
        print(f"[{t_time}] 🐶/🐱 {pet_name}: {task.description()} ({task.duration_minutes()}m) - Priority: {'⭐' * task.priority()}")
    
    print("-" * 60)

if __name__ == "__main__":
    run_demo()