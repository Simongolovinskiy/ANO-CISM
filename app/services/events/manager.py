import logging
import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
from queue import Queue

from app.domain.entities.tasks import Task
from app.domain.sql.models import Task as TaskModel
from app.infrastructure.message_brokers.base import BaseMessageBroker
from app.infrastructure.uow.base import BaseUnitOfWork

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ThreadTaskQueueManager:
    def __init__(
        self,
        uow: BaseUnitOfWork,
        broker: BaseMessageBroker,
    ):
        self.uow = uow
        self.broker = broker
        self.task_queue = Queue()
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self.executor: Optional[ThreadPoolExecutor] = None

    async def start(self):
        logging.info("Запуск менеджера очереди задач")
        self.executor = ThreadPoolExecutor()

        threading.Thread(target=self._process_queue, daemon=True).start()

        asyncio.create_task(self._consume_messages())

    async def stop(self):
        logging.info("Остановка менеджера очереди задач")
        if self.executor:
            self.executor.shutdown(wait=True)
            logging.info("Пул потоков успешно завершён")

    def _process_queue(self):
        while True:
            try:
                if not self.task_queue.empty():
                    task = self.task_queue.get()
                    logging.info(f"Задача {task.oid} извлечена из очереди и передана на выполнение")
                    self.executor.submit(self._run_task, task)
                time.sleep(0.2)
            except Exception as e:
                logging.error(f"Ошибка при обработке очереди: {e}")

    async def _consume_messages(self):
        logging.info("Начато потребление сообщений")
        async for message in self.broker.start_consuming():
            routing_key = message['routing_key']
            data = message['data']

            if routing_key == 'task.created':
                task = Task(
                    oid=data['oid'],
                    description=data['description'],
                    status=data['status']
                )
                logging.info(f"Получено сообщение о создании задачи {task.oid}")
                self.task_queue.put(task)

    def _run_task(self, task: Task):
        try:
            logging.info(f"Начало выполнения задачи {task.oid}")
            updated_task = task.run_task()
            logging.info(f"Задача {task.oid} выполнена. Статус: {updated_task.status}")
            asyncio.run_coroutine_threadsafe(
                self._async_update_task_in_db(updated_task),
                self.loop
            ).result()
            logging.info(f"Статус задачи {task.oid} обновлен в базе данных")
        except Exception as e:
            logging.error(f"Ошибка при выполнении задачи {task.oid}: {e}")

    async def _async_update_task_in_db(self, task: Task) -> None:
        try:
            async with self.uow.transaction() as uow:
                repository = uow.repository(TaskModel)
                task_to_update = await repository.get(task.oid)
                task_to_update.status = task.status
                task_to_update.start_time = task.start_time
                task_to_update.exec_time = task.exec_time
                logging.info(f"Задача {task.oid} успешно обновлена в базе данных")
        except Exception as e:
            logging.error(f"Ошибка при обновлении задачи {task.oid} в базе данных: {e}")
