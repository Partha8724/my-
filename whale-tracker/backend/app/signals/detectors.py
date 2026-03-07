from __future__ import annotations


def confidence_score(size: float, volume_mult: float, trend_alignment: float, has_oi: bool, has_liq: bool) -> int:
    score = min(40, int(size / 50000))
    score += min(20, int(volume_mult * 5))
    score += int(15 * max(-1, min(1, trend_alignment)))
    score += 12 if has_oi else 0
    score += 8 if has_liq else 0
    return max(0, min(100, score))


def large_trade_detector(event: dict, threshold: float) -> bool:
    return event.get('event_type') == 'trade' and event.get('size', 0) >= threshold


def volume_spike_detector(latest_volume: float, avg_volume: float, mult: float) -> bool:
    return avg_volume > 0 and latest_volume / avg_volume >= mult


def breakout_detector(last_price: float, highs: list[float], lows: list[float], volume_confirmed: bool) -> str | None:
    if not highs or not lows:
        return None
    if last_price > max(highs) and volume_confirmed:
        return 'bullish_breakout'
    if last_price < min(lows) and volume_confirmed:
        return 'bearish_breakdown'
    return None
