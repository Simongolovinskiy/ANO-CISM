from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, AsyncIterator, Dict


@dataclass
class BaseMessageBroker(ABC):
    @abstractmethod
    async def start(self) -> None:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...

    @abstractmethod
    async def send_message(self, routing_key: str, data: Any) -> None:
        ...

    @abstractmethod
    async def start_consuming(self) -> AsyncIterator[Dict]:
        ...

    @abstractmethod
    async def stop_consuming(self) -> None:
        ...

    async def consume(self):
        ...
