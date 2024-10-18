from dataclasses import dataclass

from app.common.enums import Status


@dataclass
class GetTasksFilters:
    limit: int = 5
    status: str = Status.completed.value
