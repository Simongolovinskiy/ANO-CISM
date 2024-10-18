from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Iterable

from app.domain.events.base import BaseEvent
from app.services.events.base import ER, ET, EventHandler


@dataclass(eq=False)
class EventMediator(ABC):
    events_map: Dict[ET, EventHandler] = field(default_factory=lambda: defaultdict(list), kw_only=True)

    @abstractmethod
    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]) -> None:
        ...

    @abstractmethod
    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        ...
