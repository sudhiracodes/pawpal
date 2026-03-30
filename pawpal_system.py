from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import List, Optional

@dataclass
class Task:
    _description: str
    _time: datetime
    _frequency: str
    _duration_minutes: int
    _priority: int  # higher = more important
    _is_complete: bool = False

    def mark_complete(self) -> None:
        """
        Marks the task as successfully completed.
        """
        self._is_complete = True
         # For recurring tasks, signal that a new instance should be created
        return self._frequency.lower() in ("daily", "weekly")
    
    def next_occurrence_time(self) -> Optional[datetime]:
        """
        Calculate the next occurrence datetime for recurring tasks.

        Returns:
            Optional[datetime]: The datetime for the next occurrence, or None if
            the task is not recurring.
        """
        freq = self._frequency.lower()
        if freq == "daily":
            # Today + 1 day at the same time of day
            return self._time + timedelta(days=1)
        elif freq == "weekly":
            # Today + 1 week at the same time of day
            return self._time + timedelta(weeks=1)
        else:
            return None


    def description(self) -> str:
        """
        Retrieves the description of the task.

        Returns:
            str: The description of the task.
        """
        return self._description

    def time(self) -> datetime:
        """
        Retrieves the scheduled datetime of the task.

        Returns:
            datetime: The time the task is scheduled for.
        """
        return self._time

    def frequency(self) -> str:
        """
        Retrieves how often the task occurs.

        Returns:
            str: The frequency of the task (e.g., 'Daily', 'Once').
        """
        return self._frequency

    def duration_minutes(self) -> int:
        """
        Retrieves the expected duration of the task.

        Returns:
            int: The duration of the task in minutes.
        """
        return self._duration_minutes

    def priority(self) -> int:
        """
        Retrieves the priority level of the task.

        Returns:
            int: The priority level (higher integer means higher priority).
        """
        return self._priority

    def is_complete(self) -> bool:
        """
        Checks if the task has been completed.

        Returns:
            bool: True if completed, False otherwise.
        """
        return self._is_complete

    def end_time(self) -> datetime:
        """
        Computes and returns the end time using the duration.

        Returns:
            datetime: The calculated end time of the task.
        """
        return self._time + timedelta(minutes=self._duration_minutes)
    
    def occurs_on(self, target_date: date) -> bool:
        """Return True if this task should be considered for target_date."""
        task_date = self._time.date()
        if self._frequency == "Once":
            return task_date == target_date
        if self._frequency == "Daily":
            # After the original start date, every day
            return target_date >= task_date
        if self._frequency == "Weekly":
            # Same weekday, on/after the original date
            return (
                target_date >= task_date
                and target_date.weekday() == task_date.weekday()
            )
        # Fallback: treat unknown frequency as "Once"
        return task_date == target_date

    def occurrence_time_on(self, target_date: date) -> datetime:
        """
        Return the datetime this task would have on target_date,
        preserving the original time-of-day.
        """
        base_time = self._time.time()
        return datetime.combine(target_date, base_time)

@dataclass
class Pet:
    _name: str
    _species: str
    _tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """
        Adds a task to the list of tasks.

        Args:
            task (Task): The task object to be added to the task list.
        """
        self._tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """
        Retrieves all tasks associated with the pet.

        Returns:
            List[Task]: A list of the pet's tasks.
        """
        return list(self._tasks)

    def name(self) -> str:
        """
        Retrieves the name of the pet.

        Returns:
            str: The pet's name.
        """
        return self._name

    def species(self) -> str:
        """
        Retrieves the species of the pet.

        Returns:
            str: The pet's species (e.g., 'Dog', 'Cat').
        """
        return self._species
    
    def get_tasks_sorted(self) -> List[Task]:
        """Return this pet's tasks sorted by time (and priority)."""
        return sorted(self._tasks, key=lambda t: (t.time(), -t.priority()))
    

@dataclass
class Owner:
    _name: str
    _pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """
        Adds a new pet to the owner's profile.

        Args:
            pet (Pet): The pet object to be added to the owner.
        """
        self._pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """
        Aggregates and returns all tasks across all owned pets.

        Returns:
            List[Task]: A flattened list of all tasks for all pets.
        """
        tasks: List[Task] = []
        for pet in self._pets:
            tasks.extend(pet.get_tasks())
        return tasks

    def name(self) -> str:
        """
        Retrieves the owner's name.

        Returns:
            str: The owner's name.
        """
        return self._name

    def pets(self) -> List[Pet]:
        """
        Retrieves the list of pets owned by the user.

        Returns:
            List[Pet]: A list of the owner's pets.
        """
        return list(self._pets)
    


@dataclass
class Scheduler:
    _owner: Owner

    
    def get_today_schedule(
        self,
        target_date: date,
        available_minutes: Optional[int] = None,
        tasks: Optional[List[Task]] = None,
    ) -> List[Task]:
        tasks_source = tasks if tasks is not None else self._owner.get_all_tasks()

        day_tasks: List[Task] = []
        for task in tasks_source:
            if task.occurs_on(target_date):
                # Create a shallow copy with today's datetime
                occurrence = Task(
                    _description=task.description(),
                    _time=task.occurrence_time_on(target_date),
                    _frequency=task.frequency(),
                    _duration_minutes=task.duration_minutes(),
                    _priority=task.priority(),
                    _is_complete=task.is_complete(),
                )
                day_tasks.append(occurrence)

        sorted_tasks = self.sort_by_time_and_priority(day_tasks)

        if available_minutes is None:
            return sorted_tasks

        chosen: List[Task] = []
        remaining = available_minutes
        for t in sorted_tasks:
            if t.duration_minutes() <= remaining:
                chosen.append(t)
                remaining -= t.duration_minutes()
            else:
                break
        return chosen


    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """
        Sorts a list of tasks strictly by their scheduled time.

        Args:
            tasks (List[Task]): The list of tasks to sort.

        Returns:
            List[Task]: The chronologically sorted list of tasks.
        """
        return sorted(tasks, key=lambda t: t.time().strftime("%H:%M"))

    # def sort_by_time_and_priority(self, tasks: List[Task]) -> List[Task]:
    #     """
    #     Sorts tasks by time, and resolves ties using priority (highest first).

    #     Args:
    #         tasks (List[Task]): The list of tasks to sort.

    #     Returns:
    #         List[Task]: The sorted list of tasks.
    #     """
    #     return sorted(tasks, key=lambda t: (t.time(), -t.priority()))

    # python

    def sort_by_time_and_priority(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: (t.time(), -t.priority(), -t.duration_minutes()))

    # def check_conflicts(self, tasks: List[Task]) -> List[Task]:
    #     """
    #     Detects tasks that start at the exact same time.

    #     Args:
    #         tasks (List[Task]): The list of tasks to check for conflicts.

    #     Returns:
    #         List[Task]: A list of tasks that have scheduling conflicts.
    #     """
    #     if not tasks:
    #         return []

    #     sorted_tasks = self.sort_by_time(tasks)
    #     conflicts: List[Task] = []

    #     for i in range(len(sorted_tasks) - 1):
    #         current = sorted_tasks[i]
    #         nxt = sorted_tasks[i + 1]
    #         if current.time() == nxt.time():
    #             if current not in conflicts:
    #                 conflicts.append(current)
    #             if nxt not in conflicts:
    #                 conflicts.append(nxt)

    #     return conflicts
    def filter_tasks(
        self,
        tasks: List[Task],
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """
        Filter tasks by completion status and/or pet name.

        Args:
            tasks: List of tasks to filter.
            completed: True -> only completed; False -> only incomplete; None -> ignore.
            pet_name: If set, only tasks belonging to this pet name.

        Returns:
            List[Task]: Filtered tasks.
        """
        filtered = tasks

        if completed is not None:
            filtered = [t for t in filtered if t.is_complete() == completed]

        if pet_name is not None:
            # Collect tasks for the given pet name
            pet_tasks: List[Task] = []
            for pet in self._owner.pets():
                if pet.name() == pet_name:
                    pet_tasks.extend(pet.get_tasks())

            # Keep only tasks that are in that pet's task list
            filtered = [t for t in filtered if t in pet_tasks]

        return filtered

    def check_conflicts(self, tasks: List[Task]) -> List[Task]:
        """
        Lightweight conflict detection.

        Detect tasks that overlap in time (for same or different pets).
        Returns a list of tasks that are in conflict. Does not raise errors.
        """
        if not tasks:
            return []

        sorted_tasks = self.sort_by_time(tasks)
        conflicts: List[Task] = []

        for i in range(len(sorted_tasks) - 1):
            current = sorted_tasks[i]
            nxt = sorted_tasks[i + 1]

            # Overlap if next starts before the current one ends
            if nxt.time() < current.end_time():
                if current not in conflicts:
                    conflicts.append(current)
                if nxt not in conflicts:
                    conflicts.append(nxt)

        return conflicts
    
   
    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """
        Mark a task complete and, if it is recurring (daily/weekly),
        create and attach a new Task instance for the next occurrence.

        Args:
            task: The Task instance to mark as complete.

        Returns:
            Optional[Task]: The newly created recurring Task, or None if no
            follow-up was created.
        """
        # Mark the original task complete
        should_repeat = task.mark_complete()

        if not should_repeat:
            return None

        next_time = task.next_occurrence_time()
        if next_time is None:
            return None

        # Create the next occurrence task
        new_task = Task(
            _description=task.description(),
            _time=next_time,
            _frequency=task.frequency(),
            _duration_minutes=task.duration_minutes(),
            _priority=task.priority(),
            _is_complete=False,
        )

        # Attach to the same pet that owns the original task
        for pet in self._owner.pets():
            if task in pet.get_tasks():
                pet.add_task(new_task)
                break

        return new_task