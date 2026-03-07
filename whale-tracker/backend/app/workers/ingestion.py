import asyncio
import logging
from datetime import datetime

from app.notifications.sender import dispatch_notifications
from app.providers.mock_provider import MockUnifiedProvider
from app.services.alert_policy import alert_policy
from app.services.analytics import analytics_engine
from app.services.engine import build_signal_card, engine
from app.services.realtime import manager
from app.services.store import admin_settings, alerts, market_cache, provider_status, signals

logger = logging.getLogger(__name__)
provider = MockUnifiedProvider()
TRACKED_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT", "DOGEUSDT", "XAUUSD", "XAGUSD"]


def _severity(confidence: int) -> str:
    if confidence >= 90:
        return "extreme"
    if confidence >= 75:
        return "high"
    if confidence >= 60:
        return "medium"
    return "low"


async def _loop_once() -> None:
    async for event in provider.subscribe_trades(TRACKED_SYMBOLS):
        symbol = event["symbol"]
        if not admin_settings.get("asset_enabled", {}).get(symbol, True):
            continue

        now = datetime.utcnow()
        analytics = analytics_engine.update(symbol, event["side"], event["size"], event["price"], now)

        snapshot = market_cache.setdefault(symbol, {"symbol": symbol, "price": event["price"], "change_24h": 0, "volume": 0, "history": [], "analytics": {}})
        snapshot["price"] = event["price"]
        snapshot["volume"] = snapshot.get("volume", 0) + event["size"]
        snapshot["last_event"] = event
        snapshot["analytics"] = analytics
        snapshot["history"] = (snapshot.get("history", []) + [{"t": now.isoformat(), "c": event["price"], "v": event["size"]}])[-200:]

        results = engine.evaluate_event(event, analytics)
        for r in results:
            signature = f"{symbol}:{r.title}:{r.direction}:{r.source_label}"
            ok, reason = alert_policy.should_emit(symbol, signature, r.confidence, now)
            if not ok:
                logger.debug("suppressed signal %s due to %s", signature, reason)
                continue

            alert = {
                "id": len(alerts) + 1,
                "asset": symbol,
                "direction": r.direction,
                "confidence": r.confidence,
                "reason": r.reason,
                "source_label": r.source_label,
                "severity": _severity(r.confidence),
                "timestamp": now.isoformat(),
                "suppression_reason": reason,
            }
            alerts.append(alert)
            signal = {"id": len(signals) + 1, **build_signal_card(symbol, r, event["price"], analytics)}
            signals.append(signal)
            await dispatch_notifications(alert)
            await manager.broadcast({"type": "alert", "payload": alert})
            await manager.broadcast({"type": "signal", "payload": signal})

        await manager.broadcast({"type": "ticker", "payload": snapshot})
        provider_status[0]["updated_at"] = now.isoformat()
        await asyncio.sleep(0)


async def run_ingestion() -> None:
    retries = 0
    while True:
        try:
            await _loop_once()
        except asyncio.CancelledError:
            logger.info("ingestion cancelled")
            raise
        except Exception as exc:
            retries += 1
            delay = min(20, 2**retries)
            provider_status[0]["status"] = "degraded"
            provider_status[0]["message"] = f"retrying after error: {exc.__class__.__name__}"
            logger.exception("ingestion error (attempt=%s), retrying in %ss", retries, delay)
            await asyncio.sleep(delay)
            if retries > 100:
                raise
