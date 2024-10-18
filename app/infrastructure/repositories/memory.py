from dataclasses import dataclass, field
from typing import List

from app.domain.entities.tasks import Task
from app.infrastructure.repositories.base import BaseTasksRepository
from app.services.exceptions.tasks import TaskNotFoundException


@dataclass
class MemoryTasksRepository(BaseTasksRepository):
    _tasks: List[Task] = field(default_factory=list, kw_only=True)

    async def add(self, task: Task) -> None:
        self._tasks.append(task)

    async def get(self, task_oid: str) -> Task | None:
        try:
            return next(task for task in self._tasks if task.oid == task_oid)
        except StopIteration:
            return

    async def update(self, task_oid: str) -> None:
        ...

    async def remove(self, task_oid: str) -> None:
        task = next(task for task in self._tasks if task.oid == task_oid)
        if not task:
            raise TaskNotFoundException(task_oid)
        self._tasks.remove(task)
