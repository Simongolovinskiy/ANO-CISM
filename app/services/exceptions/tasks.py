from dataclasses import dataclass

from app.services.exceptions.base import ServicesException


@dataclass(eq=False)
class TaskNotFoundException(ServicesException):
    task_oid: str

    @property
    def message(self):
        return f"Task with that oid does not exist - {self.task_oid}"
