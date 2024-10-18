DC = docker-compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env

APP_FILE = docker/app.yaml
DB_FILE = docker/postgresql.yaml
MESSAGE_BROKER = docker/message_broker.yaml

APP_CONTAINER = main-app
DB_CONTAINER = postgres_db
.PHONY: app
app:
	${DC} -f ${MESSAGE_BROKER} -f  ${DB_FILE} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${DB_FILE} -f ${MESSAGE_BROKER} down

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f


.PHONY: db-logs
db-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: migrations
migrations:
	${DC} -f ${DB_FILE} -f ${APP_FILE} ${ENV} run --rm ${APP_CONTAINER} alembic revision --autogenerate -m "initial"
	${DC} -f ${DB_FILE} -f ${APP_FILE} ${ENV} run --rm ${APP_CONTAINER} alembic upgrade head

.PHONY: all
all: app migrations

.DEFAULT_GOAL := all