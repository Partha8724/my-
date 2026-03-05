import asyncio
import logging
import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.db.session import SessionLocal
from app.models.entities import Event, Rule, Alert
from app.notifications.sender import send_email, send_telegram
from app.providers.base import Provider
from app.providers.ccxt_provider import CCXTTradeSpikeProvider
from app.providers.mock_provider import MockCryptoProvider, MockStockProvider, MockXAUProvider
from app.providers.real_providers import WhaleAlertProvider, TwelveDataXAUProvider
from app.rules.engine import should_trigger, dedupe_key

structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.INFO))
logger = structlog.get_logger(__name__)


class IngestionService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.last_run = None
        self.last_error = None

    def get_providers(self) -> list[Provider]:
        providers: list[Provider] = []
        providers.append(MockStockProvider() if settings.stock_provider == "mock" else MockStockProvider())
        providers.append(MockCryptoProvider() if settings.crypto_provider == "mock" else WhaleAlertProvider())
        providers.append(MockXAUProvider() if settings.xau_provider == "mock" else TwelveDataXAUProvider())
        providers.append(CCXTTradeSpikeProvider())
        return providers

    async def run_cycle(self):
        db = SessionLocal()
        try:
            for provider in self.get_providers():
                try:
                    events = await provider.fetch_events()
                    for item in events:
                        event = Event(**item.__dict__)
                        db.add(event)
                        try:
                            db.commit()
                        except IntegrityError:
                            db.rollback()
                            continue
                        await self._evaluate_rules(db, event)
                except Exception as exc:
                    self.last_error = str(exc)
                    logger.error("provider_error", provider=provider.name, error=str(exc))
            self.last_run = "ok"
        finally:
            db.close()

    async def _evaluate_rules(self, db: Session, event: Event):
        rules = db.query(Rule).filter(Rule.enabled.is_(True)).all()
        for rule in rules:
            last = db.query(Alert).filter(Alert.rule_name == rule.name).order_by(Alert.created_at.desc()).first()
            trigger, why = should_trigger(rule, event, last)
            if not trigger:
                continue
            key = dedupe_key(rule, event)
            existing = db.query(Alert).filter(Alert.dedupe_key == key).first()
            if existing:
                continue
            msg = (
                f"{event.asset_symbol} {event.event_type} size=${event.amount_usd or 0:,.0f} "
                f"time={event.timestamp.isoformat()} source={event.source} why={why}"
            )
            alert = Alert(event_uid=event.event_uid, rule_name=rule.name, dedupe_key=key, message=msg)
            db.add(alert)
            db.commit()
            alert.delivered_telegram = await send_telegram(alert)
            alert.delivered_email = await send_email(alert)
            db.commit()

    def start(self):
        self.scheduler.add_job(lambda: asyncio.create_task(self.run_cycle()), "interval", seconds=settings.poll_interval_seconds)
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown(wait=False)


ingestion_service = IngestionService()
