from celery import Celery
from app.core.config import settings

celery = Celery('whalescope', broker=settings.redis_url, backend=settings.redis_url)

@celery.task
def ping_task() -> str:
    return 'pong'
