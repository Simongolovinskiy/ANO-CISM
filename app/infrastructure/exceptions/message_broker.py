from dataclasses import dataclass

from app.infrastructure.exceptions.base import InfrastructureException


@dataclass(eq=False)
class ConnectionNotInitializedException(InfrastructureException):
    message: str

    @property
    def message(self):
        return f"Error. Connection is not initialized - {self.message}"
