from punq import Container
from pytest import fixture

from app.infrastructure.repositories.base import BaseTasksRepository
from app.services.mediator.base import Mediator
from tests.fixtures import init_test_container


@fixture()
def container() -> Container:
    return init_test_container()


@fixture()
def task_repository(container: Container) -> BaseTasksRepository:
    return container.resolve(BaseTasksRepository)


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)
