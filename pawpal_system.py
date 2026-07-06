from __future__ import annotations
from dataclasses import dataclass, field
from datetime import time
from typing import Optional


@dataclass
class Task:
    title: str
    duration: int       # minutes
    priority: int
    frequency: str

    def edit(
        self,
        title: Optional[str] = None,
        duration: Optional[int] = None,
        priority: Optional[int] = None,
        frequency: Optional[str] = None,
    ) -> Task:
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

    def add_task(self, title: str, duration: int, priority: int, frequency: str) -> Task:
        task = Task(title=title, duration=duration, priority=priority, frequency=frequency)
        self.tasks.append(task)
        return task

    def remove_task(self, task: Task) -> None:
        self.tasks.remove(task)

    def find_task(self, title: str) -> Optional[Task]:
        for task in self.tasks:
            if task.title == title:
                return task
        return None


@dataclass
class Scheduler:
    # Returns (schedule, reasoning) where schedule is list[(pet_name, time, Task)]
    def generate_schedule(self, owner: Owner) -> tuple:
        pass


@dataclass
class Owner:
    name: str
    scheduler: Scheduler = field(default_factory=Scheduler)
    pets: list[Pet] = field(default_factory=list)
    schedule: list[tuple] = field(default_factory=list)  # list[(str, time, Task)]
    reasoning: list[str] = field(default_factory=list)

    def add(self, pet: Pet) -> Pet:
        self.pets.append(pet)
        return pet

    def remove(self, pet: Pet) -> None:
        self.pets.remove(pet)

    def find_pet(self, name: str) -> Optional[Pet]:
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_tasks(self) -> list[Task]:
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

    def generate_schedule(self) -> None:
        self.schedule, self.reasoning = self.scheduler.generate_schedule(self)

    def display_schedule(self) -> None:
        for entry in self.schedule:
            print(entry)

    def display_reasoning(self) -> None:
        for reason in self.reasoning:
            print(reason)
