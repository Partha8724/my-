import logging

logger = logging.getLogger(__name__)


async def dispatch_notifications(alert: dict) -> None:
    logger.info("Notification dispatched: %s", alert)
