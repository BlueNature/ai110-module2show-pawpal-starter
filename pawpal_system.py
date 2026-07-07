from __future__ import annotations
from dataclasses import dataclass, field
from datetime import time
from enum import Enum
from typing import Optional


class Priority(Enum):
    VERY_HIGH = 5
    HIGH      = 4
    MEDIUM    = 3
    LOW       = 2
    VERY_LOW  = 1


@dataclass
class Task:
    title: str
    duration: int       # minutes
    priority: Priority
    frequency: str
    completed: bool = field(default=False)

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def edit(
        self,
        title: Optional[str] = None,
        duration: Optional[int] = None,
        priority: Optional[Priority] = None,
        frequency: Optional[str] = None,
    ) -> Task:
        """Update any subset of task fields and return the modified task."""
        if title is not None:
            self.title = title
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

    def add_task(self, title: str, duration: int, priority: Priority, frequency: str) -> Task:
        """Create a new Task, attach it to this pet, and return it."""
        task = Task(title=title, duration=duration, priority=priority, frequency=frequency)
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
    # Returns (schedule, reasoning) where schedule is list[(pet_name, time, Task)]
    def generate_schedule(self, owner: Owner) -> tuple:
        """Generate a prioritized daily schedule for all of the owner's pets."""
        pass


@dataclass
class Owner:
    name: str
    scheduler: Scheduler = field(default_factory=Scheduler)
    pets: list[Pet] = field(default_factory=list)
    schedule: list[tuple[str, time, Task]] = field(default_factory=list)  # list[(str, time, Task)]
    reasoning: list[str] = field(default_factory=list)

    def add(self, pet: Pet) -> Pet:
        """Add a pet to this owner's roster and return it."""
        self.pets.append(pet)
        return pet

    def remove(self, pet: Pet) -> None:
        """Remove a pet from this owner's roster."""
        self.pets.remove(pet)

    def find_pet(self, name: str) -> Optional[Pet]:
        """Return the pet with the given name, or None if not found."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_tasks(self) -> list[Task]:
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
