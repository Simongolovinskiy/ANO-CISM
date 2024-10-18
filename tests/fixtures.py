from punq import Container, Scope

from app.infrastructure.repositories.base import BaseTasksRepository
from app.infrastructure.repositories.memory import MemoryTasksRepository
from app.services.init import _init_container


def init_test_container() -> Container:
    container = _init_container()
    container.register(BaseTasksRepository, MemoryTasksRepository, scope=Scope.singleton)
    return container
