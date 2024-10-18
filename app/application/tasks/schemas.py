from datetime import timedelta, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.domain.entities.tasks import Task


class CreateTaskRequestSchema(BaseModel):
    description: str


class CreateTaskResponseSchema(BaseModel):
    oid: str
    description: str

    @classmethod
    def from_entity(cls, task: Task) -> "CreateTaskResponseSchema":
        return cls(oid=task.oid, description=task.description)


class TaskSchema(BaseModel):
    task_oid: str
    description: str
    status: str
    create_time: datetime
    start_time: Optional[datetime] = Field(default=None)
    exec_time: Optional[timedelta] = Field(default=None)

    class Config:
        from_attributes = True

