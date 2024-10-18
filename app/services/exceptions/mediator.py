from dataclasses import dataclass

from app.services.exceptions.base import ServicesException


@dataclass(eq=False)
class EventHandlersNotRegistered(ServicesException):
    event_type: type

    @property
    def message(self):
        return f"No event handlers registered - {self.event_type}"


@dataclass(eq=False)
class CommandHandlersNotRegistered(ServicesException):
    command_type: type

    @property
    def message(self):
        return f"No command handlers registered - {self.command_type}"
