"""In-process, ephemeral job store (no persistence)."""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass


@dataclass
class Job:
    task_id: str
    tool: str
    status: str = "queued"
    progress: int = 0
    result_url: str | None = None
    error: str | None = None


class JobStore:
    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._lock = threading.Lock()

    def create(self, tool: str) -> Job:
        job = Job(task_id=str(uuid.uuid4()), tool=tool)
        with self._lock:
            self._jobs[job.task_id] = job
        return job

    def get(self, task_id: str) -> Job | None:
        with self._lock:
            return self._jobs.get(task_id)

    def update(self, task_id: str, **changes: object) -> Job | None:
        with self._lock:
            job = self._jobs.get(task_id)
            if job is None:
                return None
            for key, value in changes.items():
                setattr(job, key, value)
            return job


store = JobStore()
