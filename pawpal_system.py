from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional

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
        # Record the pet name on the task for easier filtering and bookkeeping
        setattr(task, "pet_name", self.name)
        self.tasks.append(task)


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    completed: bool = False
    time: Optional[str] = None
    recurrence: Optional[str] = None
    pet_name: Optional[str] = None
    due_date: Optional[datetime] = None

    def __post_init__(self):
        """Validate Task fields after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title must be provided")
        if self.duration_minutes <= 0:
            raise ValueError("Task duration must be positive")
        if self.priority not in PRIORITY_RANK:
            raise ValueError(f"Unknown priority: {self.priority}")

    def mark_complete(self) -> Optional['Task']:
        """Mark this task completed.

        If the task has a recurrence of 'daily' or 'weekly', return a new Task
        instance for the next occurrence with an updated due date. Otherwise
        return None.
        """
        self.completed = True
        if self.recurrence in ("daily", "weekly"):
            next_due = None
            if self.due_date is not None:
                # preserve a relative recurrence interval from the existing due date.
                delta = timedelta(days=1 if self.recurrence == "daily" else 7)
                next_due = self.due_date + delta
            else:
                next_due = datetime.now() + timedelta(days=1 if self.recurrence == "daily" else 7)

            new_task = Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                completed=False,
                time=self.time,
                recurrence=self.recurrence,
                pet_name=self.pet_name,
                due_date=next_due,
            )
            return new_task
        return None

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

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by a common scheduled time attribute.

        This helper detects a time-like field on each Task and converts it to a
        numeric day-minute value. Tasks are ordered by that normalized time.
        If no explicit time is available, tasks are placed after scheduled
        tasks and ordered by duration so the sort is stable and predictable.
        """

        def to_minutes(val):
            if val is None:
                return float("inf")
            if isinstance(val, (int, float)):
                return float(val)
            if isinstance(val, timedelta):
                return val.total_seconds() / 60.0
            if isinstance(val, datetime):
                return val.hour * 60 + val.minute + val.second / 60.0
            # avoid shadowing datetime name
            import datetime as _dt

            if isinstance(val, _dt.time):
                return val.hour * 60 + val.minute + val.second / 60.0
            if isinstance(val, str):
                # try common time formats
                for fmt in ("%H:%M", "%H:%M:%S"):
                    try:
                        parsed = datetime.strptime(val, fmt)
                        return parsed.hour * 60 + parsed.minute + parsed.second / 60.0
                    except Exception:
                        pass
                try:
                    parsed = datetime.fromisoformat(val)
                    return parsed.hour * 60 + parsed.minute + parsed.second / 60.0
                except Exception:
                    return float("inf")
            return float("inf")

        def key_for_task(task: Task) -> float:
            for attr in ("time", "start_time", "scheduled_time", "scheduled_at"):
                if hasattr(task, attr):
                    return to_minutes(getattr(task, attr))
            # place unscheduled tasks after scheduled ones, order by duration
            return self.available_minutes + float(getattr(task, "duration_minutes", 0))

        result = sorted(tasks, key=key_for_task)
        return result

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect same-time task overlaps and return warning messages.

        This method performs lightweight conflict detection without raising an
        exception. It identifies tasks that share the same scheduled time key
        and returns a list of human-readable warnings.
        """
        occurrences = {}
        warnings: List[str] = []

        for task in tasks:
            key = None
            if task.time:
                key = (task.time, getattr(task, "due_date", None))
            elif task.due_date is not None:
                key = (task.due_date.strftime("%Y-%m-%d %H:%M"), None)

            if key is None:
                continue

            occurrences.setdefault(key, []).append(task)

        for key, task_group in occurrences.items():
            if len(task_group) > 1:
                time_label = key[0]
                description = ", ".join(
                    f"{task.title} (pet={task.pet_name or 'unknown'})"
                    for task in task_group
                )
                warnings.append(f"Conflict detected at {time_label}: {description}")

        return warnings

    def filter_tasks(self, tasks: List[Task], completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name.

        The method supports both filters at once, so it can produce lists such as
        "all incomplete tasks for a specific pet" or "all completed tasks across
        pets." If a filter is omitted, that criteria is not applied.
        """

        results = tasks
        if completed is not None:
            results = [t for t in results if bool(t.completed) is bool(completed)]
        if pet_name is not None:
            results = [t for t in results if getattr(t, "pet_name", None) == pet_name]
        return results
