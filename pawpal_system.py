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
    ) -> List[Task]:
        """
        Retrieves, filters, sorts, and budgets tasks for a specific date.

        Args:
            target_date (date): The specific date to retrieve tasks for.
            available_minutes (Optional[int], optional): The maximum time budget in minutes. Defaults to None.

        Returns:
            List[Task]: A list of scheduled tasks fitting the constraints.
        """
        day_tasks: List[Task] = []
        for task in self._owner.get_all_tasks():
            if task.time().date() == target_date:
                day_tasks.append(task)

        sorted_tasks = self.sort_by_time_and_priority(day_tasks)

        if available_minutes is None:
            return sorted_tasks

        chosen: List[Task] = []
        remaining = available_minutes
        for task in sorted_tasks:
            if task.duration_minutes() <= remaining:
                chosen.append(task)
                remaining -= task.duration_minutes()
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
        return sorted(tasks, key=lambda t: t.time())

    def sort_by_time_and_priority(self, tasks: List[Task]) -> List[Task]:
        """
        Sorts tasks by time, and resolves ties using priority (highest first).

        Args:
            tasks (List[Task]): The list of tasks to sort.

        Returns:
            List[Task]: The sorted list of tasks.
        """
        return sorted(tasks, key=lambda t: (t.time(), -t.priority()))

    def check_conflicts(self, tasks: List[Task]) -> List[Task]:
        """
        Detects tasks that start at the exact same time.

        Args:
            tasks (List[Task]): The list of tasks to check for conflicts.

        Returns:
            List[Task]: A list of tasks that have scheduling conflicts.
        """
        if not tasks:
            return []

        sorted_tasks = self.sort_by_time(tasks)
        conflicts: List[Task] = []

        for i in range(len(sorted_tasks) - 1):
            current = sorted_tasks[i]
            nxt = sorted_tasks[i + 1]
            if current.time() == nxt.time():
                if current not in conflicts:
                    conflicts.append(current)
                if nxt not in conflicts:
                    conflicts.append(nxt)

        return conflicts