from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class InfrastructureException(ApplicationException):
    @property
    def message(self):
        return "An error in infrastructure layer."
