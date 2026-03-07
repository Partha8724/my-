import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings
from app.core.logging import setup_logging
from app.workers.ingestion import run_ingestion

ingestion_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global ingestion_task
    setup_logging()
    ingestion_task = asyncio.create_task(run_ingestion())
    yield
    if ingestion_task:
        ingestion_task.cancel()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
