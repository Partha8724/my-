from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from math import log10

import httpx
from sqlalchemy.orm import Session

from app.models.entities import Alert, Asset, Event
from app.utils import utc_now


def clamp(value: float, minimum: float, maximum: float) -> float:
    return min(maximum, max(minimum, value))


def score_event(event: Event, now: datetime) -> float:
    age_hours = max((now - event.timestamp).total_seconds() / 3600, 0)
    recency_weight = clamp(1 - (age_hours / 24), 0.2, 1.0)
    amount = event.amount_usd or 0
    size_bonus = 0 if amount <= 0 else min(log10(amount + 1) * 1.8, 13)
    direction = (event.direction or "unknown").lower()
    payload = event.payload or {}

    impact = 0.0

    if event.event_type == "large_swap":
        impact += 11 if direction in {"buy", "out", "up"} else -9 if direction in {"sell", "in", "down"} else 6
    elif event.event_type == "exchange_flow":
        impact += 12 if direction == "out" else -12 if direction in {"in", "sell"} else -7
    elif event.event_type == "large_transfer":
        impact += 8 if direction == "out" else -6 if direction == "in" else 3
    elif event.event_type == "price_spike":
        impact += 9 if direction == "up" else -9 if direction == "down" else 4
    elif event.event_type == "unusual_volume":
        impact += 5 if direction == "up" else -5 if direction == "down" else 2

    impact += event.confidence * 10
    impact += min(payload.get("percent_move", 0) * 1.5, 12)
    impact += min(max(payload.get("volume_multiple", 0) - 1, 0) * 2.2, 10)
    impact += min(payload.get("volatility", 0) * 1.3, 6)
    impact += size_bonus

    return impact * recency_weight


def build_signal_summary(score: float, buy_pressure: float, sell_pressure: float) -> tuple[str, str]:
    if score >= 60:
        return "LONG", "Whale accumulation and trade activity support upside continuation."
    if score <= 40:
        return "SHORT", "Distribution pressure is stronger than accumulation across recent whale events."
    if buy_pressure > sell_pressure:
        return "WAIT", "Bullish flow exists, but conviction is not strong enough for a clean long signal."
    if sell_pressure > buy_pressure:
        return "WAIT", "Bearish flow exists, but conviction is not strong enough for a clean short signal."
    return "WAIT", "Signal quality is mixed across the latest whale events."


def event_bias(event: Event) -> str:
    direction = (event.direction or "unknown").lower()
    if event.event_type == "exchange_flow":
        return "bullish" if direction == "out" else "bearish" if direction in {"in", "sell"} else "neutral"
    if event.event_type in {"large_swap", "price_spike", "unusual_volume"}:
        return "bullish" if direction in {"buy", "up", "out"} else "bearish" if direction in {"sell", "down", "in"} else "neutral"
    if event.event_type == "large_transfer":
        return "bullish" if direction == "out" else "bearish" if direction == "in" else "neutral"
    return "neutral"


def build_trend(events: list[Event], now: datetime) -> list[float]:
    hourly_scores: list[float] = []
    for hours_back in range(5, -1, -1):
        bucket_end = now - timedelta(hours=hours_back)
        bucket_start = bucket_end - timedelta(hours=1)
        bucket_events = [event for event in events if bucket_start <= event.timestamp < bucket_end]
        if not bucket_events:
            hourly_scores.append(50.0)
            continue
        bucket_score = clamp(50 + sum(score_event(event, now) for event in bucket_events) / max(len(bucket_events), 1), 5, 95)
        hourly_scores.append(round(bucket_score, 1))
    return hourly_scores


def generate_crypto_signals(db: Session, lookback_hours: int = 24) -> list[dict]:
    now = utc_now()
    since = now - timedelta(hours=lookback_hours)

    assets = db.query(Asset).filter(Asset.asset_type == "crypto", Asset.active.is_(True)).all()
    events = (
        db.query(Event)
        .filter(Event.asset_type == "crypto", Event.timestamp >= since)
        .order_by(Event.timestamp.desc())
        .all()
    )
    alerts = (
        db.query(Alert)
        .filter(Alert.created_at >= since)
        .order_by(Alert.created_at.desc())
        .all()
    )

    symbols = {asset.symbol for asset in assets} | {event.asset_symbol for event in events}
    events_by_symbol: dict[str, list[Event]] = defaultdict(list)
    alerts_by_symbol: dict[str, list[Alert]] = defaultdict(list)

    for event in events:
        events_by_symbol[event.asset_symbol].append(event)

    for alert in alerts:
        symbol = alert.message.split(" ", 1)[0] if alert.message else "UNKNOWN"
        alerts_by_symbol[symbol].append(alert)

    signal_rows = []
    for symbol in symbols:
        symbol_events = events_by_symbol.get(symbol, [])
        if not symbol_events:
            continue
        asset = next((item for item in assets if item.symbol == symbol), None)
        total_whale_usd = sum((item.amount_usd or 0) for item in symbol_events)
        scored_events = [score_event(item, now) for item in symbol_events[:20]]
        net_flow = sum(scored_events)
        buy_pressure = sum(value for value in scored_events if value > 0)
        sell_pressure = abs(sum(value for value in scored_events if value < 0))
        alert_count = len(alerts_by_symbol.get(symbol, []))
        bullish_chance = int(round(clamp(50 + net_flow / 3 + min(alert_count * 2, 10), 5, 95)))
        bearish_chance = 100 - bullish_chance
        signal, summary = build_signal_summary(bullish_chance, buy_pressure, sell_pressure)
        last_event = symbol_events[0]
        whale_direction = (
            "accumulation"
            if buy_pressure > sell_pressure * 1.1
            else "distribution"
            if sell_pressure > buy_pressure * 1.1
            else "mixed"
        )

        signal_rows.append(
            {
                "symbol": symbol,
                "venue": asset.venue if asset else last_event.source,
                "bullish_chance": bullish_chance,
                "bearish_chance": bearish_chance,
                "signal": signal,
                "whale_direction": whale_direction,
                "total_whale_usd": round(total_whale_usd, 2),
                "event_count": len(symbol_events),
                "alert_count": alert_count,
                "last_event_type": last_event.event_type,
                "last_event_at": last_event.timestamp,
                "summary": summary,
                "sources": sorted({item.source for item in symbol_events}),
                "trend": build_trend(symbol_events, now),
            }
        )

    return sorted(signal_rows, key=lambda item: item["bullish_chance"], reverse=True)


def get_whale_orders(db: Session, symbol: str | None = None, limit: int = 30, lookback_hours: int = 24) -> list[dict]:
    since = utc_now() - timedelta(hours=lookback_hours)
    query = (
        db.query(Event)
        .filter(Event.asset_type == "crypto", Event.timestamp >= since)
        .order_by(Event.timestamp.desc())
    )
    if symbol:
        query = query.filter(Event.asset_symbol == symbol.upper())

    events = query.limit(limit).all()
    rows = []
    for event in events:
        rows.append(
            {
                "event_uid": event.event_uid,
                "symbol": event.asset_symbol,
                "event_type": event.event_type,
                "amount_usd": round(event.amount_usd or 0, 2),
                "direction": event.direction or "unknown",
                "confidence": round(event.confidence, 2),
                "source": event.source,
                "timestamp": event.timestamp,
                "from_label": event.from_label,
                "to_label": event.to_label,
                "bias": event_bias(event),
            }
        )
    return rows


def normalize_market_symbol(symbol: str) -> str:
    cleaned = symbol.upper().replace("/", "").replace("-", "")
    return cleaned if cleaned.endswith("USDT") else f"{cleaned}USDT"


async def fetch_live_market_snapshots(symbols: list[str]) -> dict[str, dict]:
    snapshots: dict[str, dict] = {}
    if not symbols:
        return snapshots

    async with httpx.AsyncClient(timeout=4.0) as client:
        for symbol in symbols:
            try:
                market_symbol = normalize_market_symbol(symbol)
                response = await client.get(
                    "https://api.binance.com/api/v3/ticker/24hr",
                    params={"symbol": market_symbol},
                )
                response.raise_for_status()
                payload = response.json()
                snapshots[symbol] = {
                    "price": float(payload.get("lastPrice", 0) or 0),
                    "change_24h": float(payload.get("priceChangePercent", 0) or 0),
                    "volume_24h": float(payload.get("quoteVolume", 0) or 0),
                    "live_supported": True,
                }
            except Exception:
                snapshots[symbol] = {
                    "price": None,
                    "change_24h": None,
                    "volume_24h": None,
                    "live_supported": False,
                }

    return snapshots


def compute_setup_quality(signal_row: dict, snapshot: dict | None) -> int:
    quality = signal_row["bullish_chance"]

    if signal_row["whale_direction"] == "accumulation":
        quality += 8
    elif signal_row["whale_direction"] == "distribution":
        quality -= 8

    quality += min(signal_row["event_count"] * 2, 10)
    quality += min(signal_row["alert_count"] * 2, 8)

    if snapshot and snapshot.get("change_24h") is not None:
        change_24h = snapshot["change_24h"]
        quality += min(max(change_24h, -6), 8)
        if change_24h < -5:
            quality -= 6

    return int(round(clamp(quality, 5, 99)))


def build_outlook(signal_row: dict, snapshot: dict | None, setup_quality: int) -> str:
    change_24h = snapshot.get("change_24h") if snapshot else None

    if signal_row["signal"] == "SHORT" and setup_quality >= 60:
        return "Bearish pressure"
    if setup_quality >= 75 and (change_24h is None or change_24h >= 0):
        return "Bullish continuation"
    if setup_quality >= 65:
        return "Bullish watch"
    if change_24h is not None and change_24h <= -4:
        return "Weak structure"
    return "Neutral watch"


def build_risk_note(signal_row: dict, snapshot: dict | None) -> str:
    change_24h = snapshot.get("change_24h") if snapshot else None

    if not snapshot or not snapshot.get("live_supported"):
        return "Live price feed unavailable, so conviction comes only from stored whale events."
    if signal_row["event_count"] <= 1:
        return "Single-event setup. Wait for more confirmation before sizing up."
    if change_24h is not None and abs(change_24h) >= 8:
        return "Price already moved hard in the last 24h, so chase risk is elevated."
    if signal_row["signal"] == "WAIT":
        return "Whale flow is mixed. Treat this as a watchlist name, not a clean trigger."
    return "Respect invalidation if whale flow flips or the next tape update loses momentum."


def build_assistant_coin(signal_row: dict, snapshot: dict | None) -> dict:
    snapshot = snapshot or {}
    setup_quality = compute_setup_quality(signal_row, snapshot)
    outlook = build_outlook(signal_row, snapshot, setup_quality)

    return {
        **signal_row,
        "outlook": outlook,
        "setup_quality": setup_quality,
        "price": snapshot.get("price"),
        "change_24h": snapshot.get("change_24h"),
        "volume_24h": snapshot.get("volume_24h"),
        "live_supported": snapshot.get("live_supported", False),
        "risk_note": build_risk_note(signal_row, snapshot),
    }


def build_assistant_brief(signal_rows: list[dict], snapshots: dict[str, dict]) -> dict:
    ranked = [build_assistant_coin(item, snapshots.get(item["symbol"])) for item in signal_rows]
    ranked.sort(key=lambda item: item["setup_quality"], reverse=True)

    best_setup = next((item for item in ranked if item["signal"] != "SHORT"), ranked[0] if ranked else None)
    best_short = next(
        (item for item in sorted(ranked, key=lambda item: item["bearish_chance"], reverse=True) if item["signal"] == "SHORT"),
        None,
    )

    commentary: list[str] = []
    if best_setup:
        price_copy = f" at ${best_setup['price']:,.4f}" if best_setup["price"] else ""
        commentary.append(
            f"{best_setup['symbol']} is the highest-quality long-side setup{price_copy} with {best_setup['bullish_chance']}% bullish odds."
        )
    if best_short:
        commentary.append(
            f"{best_short['symbol']} has the clearest bearish structure with {best_short['bearish_chance']}% downside odds."
        )
    if ranked:
        live_count = sum(1 for item in ranked if item["live_supported"])
        commentary.append(
            f"{live_count} of {len(ranked)} tracked coins currently have live Binance market snapshots attached to the whale model."
        )

    market_mode = "live" if any(item.get("live_supported") for item in ranked) else "fallback"

    return {
        "generated_at": utc_now(),
        "market_mode": market_mode,
        "best_setup": best_setup,
        "best_short": best_short,
        "watchlist": ranked[:5],
        "commentary": commentary,
    }


async def get_assistant_brief(db: Session, lookback_hours: int = 24) -> dict:
    signal_rows = generate_crypto_signals(db, lookback_hours=lookback_hours)
    symbols = [item["symbol"] for item in signal_rows[:8]]
    snapshots = await fetch_live_market_snapshots(symbols)
    return build_assistant_brief(signal_rows, snapshots)
