from dataclasses import dataclass
from typing import Type, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.tasks import Task
from app.infrastructure.filters.tasks import GetTasksFilters
from app.infrastructure.repositories.base import BaseTasksRepository


@dataclass
class SQLAlchemyTasksRepository(BaseTasksRepository):
    session: AsyncSession
    model_class: Type[Task]

    async def add(self, task: Task) -> None:
        self.session.add(task)

    async def get(self, task_oid: str) -> Task | None:
        query = select(self.model_class).filter_by(task_oid=task_oid)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def fetch_all(self, filters: GetTasksFilters) -> List[Task]:
        status = filters.status
        limit = filters.limit

        query = select(self.model_class).filter_by(status=status).limit(limit)
        result = await self.session.execute(query)
        
        return list(result.scalars().fetchall())

    async def update(self, task_oid: str) -> None:
        ...

    async def remove(self, task_oid: str) -> None:
        ...
