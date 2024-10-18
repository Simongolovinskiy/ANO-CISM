from contextlib import asynccontextmanager

from app.infrastructure.message_brokers.base import BaseMessageBroker
from app.services.events.manager import ThreadTaskQueueManager
from app.services.init import init_container


async def start_message_broker():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.start()


async def stop_message_broker():
    container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.close()


async def start_manager():
    container = init_container()
    manager = container.resolve(ThreadTaskQueueManager)
    await manager.start()


async def stop_manager():
    container = init_container()
    manager = container.resolve(ThreadTaskQueueManager)
    await manager.stop()


@asynccontextmanager
async def lifespan(*_):
    await start_message_broker()
    await start_manager()
    yield
    await stop_message_broker()
    await stop_manager()
