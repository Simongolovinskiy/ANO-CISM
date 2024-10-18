from contextlib import asynccontextmanager
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.tasks import Task
from app.infrastructure.uow.sample import UnitOfWork


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session
        self.cache: List[Task] = list()

    async def commit(self) -> None:
        await super().commit()
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    @asynccontextmanager
    async def transaction(self):
        try:
            yield self
            await self.commit()
        except Exception:
            await self.rollback()
            raise
        finally:
            await self.session.close()

    def push_to_cache(self, task: Task) -> None:
        self.cache.append(task)

    def remove_task_from_cache(self, current_task: Task) -> None:
        [self.cache.pop() for task in self.cache if current_task == task]

    def get_task_from_cache(self, task_oid: str) -> Task | None:
        task = [task for task in self.cache if task.oid == task_oid]
        return task[0] if task else None
