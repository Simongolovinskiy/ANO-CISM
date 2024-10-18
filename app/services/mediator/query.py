from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict

from app.services.queries.base import QR, QT, QueryHandler


@dataclass(eq=False)
class QueryMediator(ABC):
    queries_map: Dict[QT, QueryHandler] = field(default_factory=dict, kw_only=True)

    @abstractmethod
    def register_query(self, query: QT, query_handler: QueryHandler[QT, QR]) -> None:
        ...

    @abstractmethod
    async def handle_query(self, query: QT) -> QR:
        ...
