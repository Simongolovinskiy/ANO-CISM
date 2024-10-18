import time
import random

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from app.common.enums import Status
from app.domain.entities.base import BaseEntity
from app.domain.events.tasks import NewTaskCreatedEvent


@dataclass(eq=False)
class Task(BaseEntity):
    start_time: datetime = field(default=None)
    exec_time: timedelta = field(default=None)
    status: str = field(default=None)

    def run_task(self) -> "Task":
        self.status = Status.run.value
        start_time = datetime.now()
        self.start_time = start_time
        time.sleep(random.randint(0, 10))
        exec_time = datetime.now() - start_time
        self.exec_time = exec_time
        self.status = random.choice([Status.completed.value, Status.failed.value])
        return self

    @classmethod
    def create_task(cls, status: str, description: str) -> "Task":
        new_task = cls(status=status, description=description)
        new_task.register_event(NewTaskCreatedEvent(task=new_task))
        return new_task
