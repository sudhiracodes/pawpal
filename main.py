
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
    midday = datetime.combine(date.today(), time(12, 0))
    afternoon = datetime.combine(date.today(), time(14, 0))

    # 3. Add Tasks to specific pets (intentionally OUT OF ORDER)
    # Whiskers' Tasks (out of order):
    whiskers.add_task(Task("Brush Fur", afternoon, "Weekly", 15, 3))
    whiskers.add_task(Task("Playtime", midday, "Daily", 20, 2))
    whiskers.add_task(Task("Feed Breakfast", early_morning, "Daily", 10, 5))


     # Fido's Tasks (out of order):
    fido.add_task(Task("Vet Visit", afternoon, "Once", 60, 5))
    fido.add_task(Task("Evening Walk", midday, "Daily", 25, 3))
    fido.add_task(Task("Morning Walk", morning, "Daily", 30, 4))
    # Intentional conflict: another task at the same time as Morning Walk
    fido.add_task(Task("Medication", morning, "Daily", 10, 2))

    # 4. Schedule and Print
    scheduler = Scheduler(owner)

    print("\n🐾 PAWPAL+ TODAY'S SCHEDULE (SORTED BY TIME & PRIORITY) 🐾")
    print("-" * 70)

    today = date.today()
    schedule = scheduler.get_today_schedule(today)

    for task in schedule:
        # Find which pet owns this specific task
        pet_name = "Unknown"
        for pet in owner.pets():
            if task in pet.get_tasks():
                pet_name = pet.name()
                break

        t_time = task.time().strftime('%H:%M')
        print(
            f"[{t_time}] {pet_name}: {task.description()} "
            f"({task.duration_minutes()}m) - Priority: {'⭐' * task.priority()}"
        )

    print("-" * 70)

       

    # Detect and print lightweight conflict warnings
    conflicts = scheduler.check_conflicts(schedule)
    if conflicts:
        print("\n⚠️  CONFLICT WARNINGS")
        for task in conflicts:
            # Figure out which pet owns this task
            pet_name = "Unknown"
            for pet in owner.pets():
                if task in pet.get_tasks():
                    pet_name = pet.name()
                    break

            t_time = task.time().strftime('%H:%M')
            print(f" - Conflict at {t_time} for {pet_name}: {task.description()}")
    else:
        print("\nNo conflicts detected.")

    # 5. Demonstrate filtering by completion status
    print("\n✅ INCOMPLETE TASKS ONLY (FILTERED)")
    # (All tasks start incomplete, so this should match the full schedule)
    incomplete_tasks = scheduler.filter_tasks(schedule, completed=False)
    for task in incomplete_tasks:
        pet_name = "Unknown"
        for pet in owner.pets():
            if task in pet.get_tasks():
                pet_name = pet.name()
                break

        t_time = task.time().strftime('%H:%M')
        print(f"[{t_time}] {pet_name}: {task.description()}")

    # 6. Demonstrate filtering by pet name
    print("\n🐶 TASKS FOR FIDO ONLY (FILTERED)")
    fido_tasks = scheduler.filter_tasks(schedule, pet_name="Fido")
    for task in fido_tasks:
        t_time = task.time().strftime('%H:%M')
        print(f"[{t_time}] Fido: {task.description()}")

    print("-" * 70)

     # 7. Demonstrate auto-creation of next occurrence for a daily task
    print("\n🔁 MARKING A DAILY TASK COMPLETE AND CREATING NEXT OCCURRENCE")
    # Pick one daily task (e.g., Fido's Morning Walk)
    daily_task = None
    for pet in owner.pets():
        for t in pet.get_tasks():
            if t.frequency().lower() == "daily":
                daily_task = t
                break
        if daily_task:
            break

    if daily_task:
        print(f"Completing task: {daily_task.description()} at {daily_task.time()}")
        new_task = scheduler.mark_task_complete(daily_task)
        if new_task:
            print(
                f"New occurrence created for: {new_task.description()} "
                f"at {new_task.time()}"
            )
        else:
            print("No new occurrence created.")
    else:
        print("No daily task found to demonstrate auto-creation.")


if __name__ == "__main__":
    run_demo()