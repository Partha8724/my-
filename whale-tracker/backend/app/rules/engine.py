from datetime import datetime

from app.models.entities import Rule, Event, Alert


def in_quiet_hours(now: datetime, quiet_hours: list[list[int]]) -> bool:
    for start, end in quiet_hours:
        if start <= now.hour < end:
            return True
    return False


def should_trigger(rule: Rule, event: Event, last_alert: Alert | None = None) -> tuple[bool, str]:
    if not rule.enabled:
        return False, "rule disabled"
    if rule.asset_type != "any" and rule.asset_type != event.asset_type:
        return False, "asset_type mismatch"
    if rule.symbol != "*" and rule.symbol != event.asset_symbol:
        return False, "symbol mismatch"
    if in_quiet_hours(datetime.utcnow(), rule.quiet_hours or []):
        return False, "quiet hours"

    if last_alert and (datetime.utcnow() - last_alert.created_at).total_seconds() < rule.cooldown_minutes * 60:
        return False, "cooldown"

    payload = event.payload or {}
    if rule.threshold_usd and (event.amount_usd or 0) < rule.threshold_usd:
        return False, "below usd threshold"
    if rule.percent_move and payload.get("percent_move", 0) < rule.percent_move:
        return False, "below percent move"
    if rule.volume_multiple and payload.get("volume_multiple", 0) < rule.volume_multiple:
        return False, "below volume multiple"
    if rule.volatility_threshold and payload.get("volatility", 0) < rule.volatility_threshold:
        return False, "below volatility threshold"
    if rule.key_levels:
        price = payload.get("price")
        if price is None:
            return False, "no price for key level"
        broken = any(abs(price - level) / level < 0.001 for level in rule.key_levels)
        if not broken:
            return False, "no key level break"

    return True, "triggered"


def dedupe_key(rule: Rule, event: Event) -> str:
    ts_bucket = int(event.timestamp.timestamp() // 300)
    return f"{rule.name}:{event.asset_symbol}:{event.event_type}:{ts_bucket}"
