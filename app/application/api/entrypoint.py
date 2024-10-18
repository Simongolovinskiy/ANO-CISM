from fastapi import FastAPI

from app.application.lifespan import lifespan
from app.application.tasks.handlers import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Task Scheduler API",
        docs_url="/api/docs",
        description="Simple scheduler with no using celery-like technologies",
        debug=True,
        lifespan=lifespan
    )

    app.include_router(router, prefix="/tasks")
    return app
