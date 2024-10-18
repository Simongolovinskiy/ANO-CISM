from dataclasses import dataclass
from typing import AsyncIterator, Dict, Optional, Any
import aio_pika
from aio_pika.abc import AbstractChannel, AbstractConnection, AbstractQueue, AbstractExchange
import orjson
from .base import BaseMessageBroker
from ..exceptions.message_broker import ConnectionNotInitializedException


@dataclass
class RabbitMQMessageBroker(BaseMessageBroker):
    url: str
    connection: Optional[AbstractConnection] = None
    channel: Optional[AbstractChannel] = None
    exchange: Optional[AbstractExchange] = None
    queue: Optional[AbstractQueue] = None
    QUEUE_NAME: str = "main_queue"
    EXCHANGE_NAME: str = "main_exchange"
    is_initialized: bool = False

    @classmethod
    def create(cls, url: str) -> 'RabbitMQMessageBroker':
        return cls(url=url)

    async def ensure_connected(self) -> None:
        """
        Метод для обеспечения подключения к брокеру
        """
        if not self.is_initialized:
            await self.start()
            self.is_initialized = True

    async def start(self) -> None:
        if not self.channel:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=1)

            self.exchange = await self.channel.declare_exchange(
                self.EXCHANGE_NAME,
                type=aio_pika.ExchangeType.TOPIC,
                durable=True
            )

            self.queue = await self.channel.declare_queue(
                self.QUEUE_NAME,
                durable=True
            )

            await self.queue.bind(self.exchange, routing_key='#')

    async def close(self) -> None:
        if self.channel:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
        self.is_initialized = False

    async def send_message(self, routing_key: str, data: Any) -> None:
        """
        Отправка сообщения в очередь
        :param routing_key: ключ маршрутизации (например: 'task.created')
        :param data: данные для отправки (будут сериализованы в JSON)
        """
        await self.ensure_connected()

        if not self.channel or not self.exchange:
            raise ConnectionNotInitializedException("Broker not initialized")

        message = aio_pika.Message(
            body=orjson.dumps(data),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        await self.exchange.publish(
            message,
            routing_key=routing_key,
        )

    async def start_consuming(self) -> AsyncIterator[Dict]:
        """
        Начало потребления сообщений из очереди
        :return: генератор сообщений
        """
        await self.ensure_connected()

        if not self.channel or not self.queue:
            raise ConnectionNotInitializedException("Broker not initialized")

        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = orjson.loads(message.body)
                    routing_key = message.routing_key
                    yield {
                        'routing_key': routing_key,
                        'data': data
                    }

    async def stop_consuming(self) -> None:
        if self.queue:
            await self.queue.cancel(self.QUEUE_NAME)
