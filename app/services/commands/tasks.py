from dataclasses import dataclass, field

from app.common.enums import Status
from app.domain.entities.tasks import Task
from app.services.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class CreateTaskCommand(BaseCommand):
    description: str
    status: str = field(default=Status.in_queue.value)


@dataclass(frozen=True)
class CreateTaskCommandHandler(CommandHandler[CreateTaskCommand, Task]):

    async def handle(self, command: CreateTaskCommand) -> Task:
        new_task = Task.create_task(status=command.status, description=command.description)

        await self._mediator.publish(new_task.pull_events())
        return new_task
