from contextlib import asynccontextmanager
from typing import Generic, TypeVar

from abc import ABC, abstractmethod

ModelT = TypeVar('ModelT')


class BaseUnitOfWork(ABC):

    @abstractmethod
    def register_dirty(self, model: ModelT) -> None:
        ...

    @abstractmethod
    def register_deleted(self, model: ModelT) -> None:
        ...

    @abstractmethod
    def register_new(self, model: ModelT) -> 'UoWModel[ModelT]':
        ...

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...

    @asynccontextmanager
    async def transaction(self):
        try:
            yield self
            await self.commit()
        except Exception:
            await self.rollback()
            raise


class UoWModel(Generic[ModelT]):
    def __init__(self, model: ModelT, uow):
        self.__dict__["_model"] = model
        self.__dict__["_uow"] = uow

    def __getattr__(self, key: str):
        return getattr(self._model, key)

    def __setattr__(self, key: str, value):
        setattr(self._model, key, value)
        self._uow.register_dirty(self._model)
