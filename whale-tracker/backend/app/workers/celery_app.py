from celery import Celery
from app.core.config import settings

celery_app = Celery('whalescope', broker=settings.redis_url, backend=settings.redis_url)


@celery_app.task
def heartbeat() -> str:
    return 'ok'
