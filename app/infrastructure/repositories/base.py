from dataclasses import dataclass
from abc import ABC, abstractmethod

from app.domain.entities.tasks import Task


@dataclass
class BaseTasksRepository(ABC):
    @abstractmethod
    async def add(self, task: Task) -> None:
        ...

    @abstractmethod
    async def get(self, task_oid: str) -> Task:
        ...

    @abstractmethod
    async def update(self, task_oid: str) -> None:
        ...

    @abstractmethod
    async def remove(self, task_oid: str) -> None:
        ...
