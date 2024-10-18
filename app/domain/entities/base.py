from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import uuid4

from app.domain.events.base import BaseEvent


@dataclass(eq=False)
class BaseEntity(ABC):
    oid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    created_at: datetime = field(default_factory=lambda: datetime.now(), kw_only=True)
    description: str = field(default=None)
    _events: List[BaseEvent] = field(default_factory=list, kw_only=True)

    def pull_events(self) -> List[BaseEvent]:
        registered_events = self._events.copy()
        self._events.clear()
        return registered_events

    def register_event(self, event: BaseEvent) -> None:
        self._events.append(event)

    def __hash__(self) -> int:
        return hash(self.oid)

    # def __eq__(self, other: "BaseEntity") -> bool:
    #     return self.oid == other.oid
