from dataclasses import dataclass

from app.domain.entities.tasks import Task
from app.domain.sql.models import Task as TaskModel

from app.domain.events.tasks import NewTaskCreatedEvent
from app.infrastructure.message_brokers.base import BaseMessageBroker
from app.infrastructure.uow.base import BaseUnitOfWork


@dataclass
class NewTaskCreatedEventHandler:
    broker: BaseMessageBroker
    uow: BaseUnitOfWork

    async def handle(self, event: NewTaskCreatedEvent) -> None:
        await self.__add_to_database(event.task)
        await self.broker.send_message("task.created", event.task)

    async def __add_to_database(self, task: Task):
        async with self.uow.transaction() as uow:
            uow.register_new(TaskModel(
                task_oid=task.oid,
                description=task.description,
                start_time=task.start_time,
                create_time=task.created_at,
                exec_time=task.exec_time,
                status=task.status
            )
            )
