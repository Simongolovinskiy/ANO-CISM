from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from app.services.mediator.event import EventMediator


@dataclass(frozen=True, eq=False)
class BaseCommand(ABC):
    ...


CT = TypeVar("CT", bound=BaseCommand)
CR = TypeVar("CR", bound=Any)


@dataclass(frozen=True)
class CommandHandler(ABC, Generic[CT, CR]):
    _mediator: EventMediator

    @abstractmethod
    async def handle(self, command: CT) -> CR:
        ...
