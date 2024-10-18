from dataclasses import dataclass
from typing import List

from app.domain.entities.tasks import Task

from app.domain.sql.models import Task as TaskModel
from app.infrastructure.filters.tasks import GetTasksFilters
from app.infrastructure.uow.base import BaseUnitOfWork
from app.services.exceptions.tasks import TaskNotFoundException
from app.services.queries.base import BaseQuery, QueryHandler


@dataclass(frozen=True)
class GetTaskDetailQuery(BaseQuery):
    task_oid: str


@dataclass(frozen=True)
class GetTasksQuery(BaseQuery):
    filters: GetTasksFilters


@dataclass(frozen=True)
class GetTaskDetailQueryHandler(QueryHandler):
    uow: BaseUnitOfWork

    async def handle(self, query: GetTaskDetailQuery) -> Task:
        task_oid = query.task_oid
        async with self.uow.transaction() as uow:
            repository = uow.repository(TaskModel)
            task = await repository.get(query.task_oid)
            if not task:
                raise TaskNotFoundException(task_oid)
        return task.to_dict()


@dataclass(frozen=True)
class GetTasksQueryHandler(QueryHandler):
    uow: BaseUnitOfWork

    async def handle(self, query: GetTasksQuery) -> List[Task]:
        async with self.uow.transaction() as uow:
            tasks = await uow.repository(TaskModel).fetch_all(query.filters)
            tasks = [task.to_dict() for task in tasks]
        return tasks
