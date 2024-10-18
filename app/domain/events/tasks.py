from dataclasses import dataclass, field
from typing import ClassVar

from app.domain.events.base import BaseEvent


@dataclass
class NewTaskReceivedEvent(BaseEvent):
    task_oid: str
    title: ClassVar[str] = "New Task Received"


@dataclass
class NewTaskCreatedEvent(BaseEvent):
    task: None = field(default=None)
    title: ClassVar[str] = "New Task Created"
