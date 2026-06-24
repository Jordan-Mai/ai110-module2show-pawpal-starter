from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List

PRIORITY_RANK = {"high": 3, "medium": 2, "low": 1}
DEFAULT_DAY_MINUTES = 8 * 60


@dataclass
class Owner:
    name: str


@dataclass
class Pet:
    name: str
    species: str
    owner: Owner
    tasks: List['Task'] = field(default_factory=list)

    def add_task(self, task: 'Task') -> None:
        """Attach a Task to this pet."""
        self.tasks.append(task)


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    completed: bool = False

    def __post_init__(self):
        """Validate Task fields after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title must be provided")
        if self.duration_minutes <= 0:
            raise ValueError("Task duration must be positive")
        if self.priority not in PRIORITY_RANK:
            raise ValueError(f"Unknown priority: {self.priority}")

    def mark_complete(self) -> None:
        """Mark this task completed."""
        self.completed = True

    @property
    def priority_value(self) -> int:
        """Return numeric priority value for sorting."""
        return PRIORITY_RANK[self.priority]

    def priority_label(self) -> str:
        """Return the human-friendly priority label."""
        return self.priority.capitalize()


@dataclass
class ScheduledTask:
    task: Task
    start_time: str
    end_time: str


@dataclass
class Schedule:
    owner: Owner
    pet: Pet
    entries: List[ScheduledTask]
    skipped_tasks: List[Task]
    explanation: str
    start_time: str

    @property
    def total_planned_minutes(self) -> int:
        """Compute total minutes planned in the schedule."""
        return sum(entry.task.duration_minutes for entry in self.entries)

    def summary_lines(self) -> List[str]:
        """Return concise human-readable summary lines for each entry."""
        return [
            f"{entry.start_time} — {entry.task.title} "
            f"({entry.task.duration_minutes} min) [priority: {entry.task.priority}]"
            for entry in self.entries
        ]


class Scheduler:
    def __init__(self, start_time: str = "08:00", available_minutes: int = DEFAULT_DAY_MINUTES):
        """Initialize scheduler with a start time and available minutes."""
        self.start_time = start_time
        self.available_minutes = available_minutes

    def build_schedule(self, owner: Owner, pet: Pet, tasks: List[Task]) -> Schedule:
        """Build a schedule for the given owner, pet and list of tasks."""

        sorted_tasks = sorted(
            tasks,
            key=lambda task: (-task.priority_value, task.duration_minutes, task.title.lower()),
        )

        current_time = datetime.strptime(self.start_time, "%H:%M")
        entries: List[ScheduledTask] = []
        skipped_tasks: List[Task] = []
        remaining_minutes = self.available_minutes

        for task in sorted_tasks:
            if task.duration_minutes <= remaining_minutes:
                end_time = current_time + timedelta(minutes=task.duration_minutes)
                entries.append(
                    ScheduledTask(
                        task=task,
                        start_time=current_time.strftime("%H:%M"),
                        end_time=end_time.strftime("%H:%M"),
                    )
                )
                current_time = end_time
                remaining_minutes -= task.duration_minutes
            else:
                skipped_tasks.append(task)

        explanation = self._build_explanation(entries, skipped_tasks)
        return Schedule(
            owner=owner,
            pet=pet,
            entries=entries,
            skipped_tasks=skipped_tasks,
            explanation=explanation,
            start_time=self.start_time,
        )

    def _build_explanation(self, entries: List[ScheduledTask], skipped_tasks: List[Task]) -> str:
        """Create a short explanation describing scheduled and skipped tasks."""

        lines = [
            f"Daily plan starts at {self.start_time} for {len(entries)} task(s).",
            f"Available day length: {self.available_minutes} minutes.",
        ]

        if entries:
            lines.append(
                f"Scheduled {len(entries)} task(s): "
                + ", ".join(entry.task.title for entry in entries)
                + "."
            )
        else:
            lines.append("No tasks could be scheduled within the available time.")

        if skipped_tasks:
            lines.append(
                f"Skipped {len(skipped_tasks)} task(s) because time ran out: "
                + ", ".join(task.title for task in skipped_tasks)
                + "."
            )

        return "\n".join(lines)
