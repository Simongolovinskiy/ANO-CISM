![Repository Top Language](https://img.shields.io/github/languages/top/Simongolovinskiy/ANO-CISM)
![Python version](https://img.shields.io/badge/python-3.10-blue.svg)
![Github Repository Size](https://img.shields.io/github/repo-size/Simongolovinskiy/ANO-CISM)
![Github Open Issues](https://img.shields.io/github/issues/Simongolovinskiy/ANO-CISM)
![License](https://img.shields.io/badge/license-MIT-green)
![GitHub last commit](https://img.shields.io/github/last-commit/Simongolovinskiy/ANO-CISM)
![GitHub contributors](https://img.shields.io/github/contributors/Simongolovinskiy/ANO-CISM)
![Simply the best](https://img.shields.io/badge/simply-the%20best%20%3B%29-orange)

<img align="right" width="50%" src="images/image.jpg">

# ANO CISM

## Description
```
Описание
Необходимо разработать сервис для управления задачами с следующими функциональными требованиями:
1.	Создание задач через REST API
2.	Создание задач через очереди сообщений (RabbitMQ или Kafka)
3.	Реализация статусной модели для задач:
a.	Новая задача
b.	В процессе работы
c.	Завершено успешно
d.	Ошибка
4.	Эмуляция процесса обработки задачи

Технические требования
1.	Язык программирования:   Python
2.	База данных: PostgreSQL
3.	Очередь сообщений: RabbitMQ или Kafka
4.	REST API: Реализовать с использованием соответствующего фреймворка (Flask, FastApi, Django)
5.	Документация API: Swagger/OpenAPI
6.	Контейнеризация: Docker

Задачи
1.	Разработать структуру базы данных для хранения задач и их статусов
2.	Реализовать REST API с следующими эндпоинтами:
a.	POST /tasks - создание новой задачи
b.	GET /tasks/{id} - получение информации о задаче
c.	GET /tasks - получение списка задач с возможностью фильтрации по статусу
3.	Реализовать создание задач через очередь сообщений
4.	Разработать worker для обработки задач:
a.	Получение задачи из очереди
b.	Изменение статуса задачи на "В процессе работы"
c.	Эмуляция выполнения задачи (например, случайная задержка 5-10 секунд)
d.	Изменение статуса задачи на "Завершено успешно" или "Ошибка" (с некоторой вероятностью)
5.	Реализовать логирование процесса обработки задач
6.	Написать unit-тесты для ключевых компонентов
7.	Подготовить Docker Compose файл для запуска всех компонентов системы

```

## Явные плюсы проекта

- :trident: Чистая архитектура
- :book: Приложение автоматически разворачивается в docker-compose
- :cd: Есть Makefile (чтобы развернуть тестовый стенд необходимо ввести всего лишь одну команду)
- :card_file_box: Великолепное ReadME

## Дополнительные фишки
- Реализованы паттерны проектирования для взаймодействия с БД - Unit of work, Repository
- Реализован паттерн Mediator для корректного взаймодействия между командами и эвентами
- Код соответствует принципу SOLID, особенно разделение интерфейсов и инверсия зависимостей
- Для иньекции зависимостей присутствует отдельный кэширующийся контейнер для того, чтобы не плодить логику в views

## Url для навигации
```http://localhost:8000/api/docs - Swagger```

## HOWTO

- Создайте файл .env и передайте туда параметры, которые указаны в файле .env.example
- Запустите проект с помощью команды `make all` - создаст сразу и контейнеры и применит миграции.
- логи uvicorn можно посмотреть при помощи команды `make app-logs`
- Залезть в контейнер можно с помощью команды `make app-shell`