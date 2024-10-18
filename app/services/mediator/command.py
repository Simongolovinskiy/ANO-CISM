from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Iterable

from app.services.commands.base import CR, CT, CommandHandler


@dataclass(eq=False)
class CommandMediator(ABC):
    commands_map: Dict[CT, CommandHandler] = field(default_factory=lambda: defaultdict(list), kw_only=True)

    @abstractmethod
    def register_command(self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]) -> None:
        ...

    @abstractmethod
    async def handle_command(self, command: CT) -> Iterable[CR]:
        ...
