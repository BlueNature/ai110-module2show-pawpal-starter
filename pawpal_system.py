from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date as Date, time as Time, timedelta
from enum import Enum
from typing import Optional


class Priority(Enum):
    VERY_HIGH = 5
    HIGH      = 4
    MEDIUM    = 3
    LOW       = 2
    VERY_LOW  = 1


class Frequency(Enum):
    DAILY    = "daily"
    WEEKLY   = "weekly"
    ONE_TIME = "one-time"


@dataclass
class Task:
    title: str
    date: Optional[Date] = field(default=None)
    time: Optional[Time] = field(default=None)
    duration: int = 0           # minutes
    priority: Priority = Priority.MEDIUM
    frequency: Frequency = Frequency.DAILY
    pet: Optional[Pet] = field(default=None, repr=False)
    completed: bool = field(default=False)

    def mark_complete(self):
        """Mark this task as completed and replace with the next iteration if necessary."""
        self.completed = True
        if self.pet is None:
            return
        if self.frequency == Frequency.WEEKLY:
            self.pet.add_task(title=self.title, date=self.date + timedelta(days=7), time=self.time, duration=self.duration, priority=self.priority, frequency=self.frequency)
        elif self.frequency == Frequency.DAILY:
            self.pet.add_task(title=self.title, date=self.date + timedelta(days=1), time=self.time, duration=self.duration, priority=self.priority, frequency=self.frequency)

    def edit(
        self,
        title: Optional[str] = None,
        date: Optional[Date] = None,
        time: Optional[Time] = None,
        duration: Optional[int] = None,
        priority: Optional[Priority] = None,
        frequency: Optional[Frequency] = None,
    ) -> Task:
        """Update any subset of task fields and return the modified task."""
        if title is not None:
            self.title = title
        if date is not None:
            self.date = date
        if time is not None:
            self.time = time
        if duration is not None:
            self.duration = duration
        if priority is not None:
            self.priority = priority
        if frequency is not None:
            self.frequency = frequency
        return self


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, *, title: str, date: Optional[Date] = None, time: Optional[Time] = None, duration: int, priority: Priority, frequency: Frequency) -> Task:
        """Create a new Task, attach it to this pet, and return it."""
        task = Task(title=title, date=date, time=time, duration=duration, priority=priority, frequency=frequency)
        task.pet = self
        self.tasks.append(task)
        return task

    def remove_task(self, task: Task) -> None:
        """Remove the given task from this pet's task list."""
        self.tasks.remove(task)

    def find_task(self, title: str) -> Optional[Task]:
        """Return the first task matching the given title, or None if not found."""
        for task in self.tasks:
            if task.title == title:
                return task
        return None


@dataclass
class Scheduler:
    # Sort and filter are static: they operate purely on a task list and need no
    # Scheduler state, but belong here so they're co-located with generate_schedule.

    @staticmethod
    def sort_by_date(tasks: list[Task]) -> list[Task]:
        """Return tasks sorted ascending by date; tasks with no date sort last."""
        return sorted(tasks, key=lambda t: t.date or Date.max)

    @staticmethod
    def sort_by_time(tasks: list[Task]) -> list[Task]:
        """Return tasks sorted ascending by time; tasks with no time sort last."""
        return sorted(tasks, key=lambda t: t.time or Time.max)

    @staticmethod
    def sort_by_priority(tasks: list[Task]) -> list[Task]:
        """Return tasks sorted descending by priority (VERY_HIGH first)."""
        return sorted(tasks, key=lambda t: t.priority.value, reverse=True)

    @staticmethod
    def sort_by_time_with_priority(tasks: list[Task]) -> list[Task]:
        """Return tasks sorted ascending by time; higher priority breaks ties."""
        return sorted(tasks, key=lambda t: (t.time or Time.max, -t.priority.value))

    @staticmethod
    def filter_by_completed(tasks: list[Task], completed: bool = True) -> list[Task]:
        """Return only tasks whose completed flag matches the given value."""
        return [t for t in tasks if t.completed == completed]

    @staticmethod
    def filter_by_date(tasks: list[Task], target_date: Date) -> list[Task]:
        """Return only tasks scheduled on target_date."""
        return [t for t in tasks if t.date == target_date]

    @staticmethod
    def filter_by_pet(tasks: list[Task], pet_name: str) -> list[Task]:
        """Return only tasks belonging to the pet with the given name."""
        return [t for t in tasks if t.pet is not None and t.pet.name == pet_name]

    def generate_schedule(self, owner: Owner) -> tuple:
        """Generate a prioritized daily schedule for all of the owner's pets."""
        pass


@dataclass
class Owner:
    name: str
    scheduler: Scheduler = field(default_factory=Scheduler)
    pets: list[Pet] = field(default_factory=list)
    schedule: list[Task] = field(default_factory=list)
    reasoning: list[str] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> Pet:
        """Add a pet to this owner's roster and return it."""
        self.pets.append(pet)
        return pet

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's roster."""
        self.pets.remove(pet)

    def find_pet(self, name: str) -> Optional[Pet]:
        """Return the pet with the given name, or None if not found."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_all_tasks(self) -> list[Task]:
        """Return a flat list of every task across all of this owner's pets."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

    def get_tasks(self, pet: Pet) -> list[Task]:
        """Return the task list for the given pet."""
        return pet.tasks

    def generate_schedule(self) -> None:
        """Invoke the scheduler and store the resulting schedule and reasoning."""
        self.schedule, self.reasoning = self.scheduler.generate_schedule(self)

    def display_schedule(self) -> None:
        """Print each scheduled entry to stdout."""
        for entry in self.schedule:
            print(entry)

    def display_reasoning(self) -> None:
        """Print each reasoning step from the last schedule generation to stdout."""
        for reason in self.reasoning:
            print(reason)
