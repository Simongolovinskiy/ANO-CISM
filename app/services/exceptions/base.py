from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class ServicesException(ApplicationException):
    @property
    def message(self):
        return "An error in handling query."
