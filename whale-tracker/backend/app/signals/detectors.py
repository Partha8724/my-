from dataclasses import dataclass


@dataclass
class DetectionResult:
    title: str
    direction: str
    confidence: int
    reason: str
    severity: str
    source_label: str


def score_confidence(size: float, volume_ratio: float, oi_change: float, liquidation_bias: float, trend_alignment: float) -> int:
    raw = (
        min(size / 1_000_000, 1) * 20
        + min(volume_ratio / 3, 1) * 20
        + min(abs(oi_change) / 10, 1) * 15
        + min(abs(liquidation_bias) / 3_000_000, 1) * 15
        + min(abs(trend_alignment), 1) * 30
    )
    return max(1, min(100, int(raw)))


def large_trade_detector(event: dict, threshold: float) -> DetectionResult | None:
    if event["size"] < threshold:
        return None
    is_buy = event.get("side") == "buy"
    confidence = score_confidence(event["size"], 2.5, 2.0, 500_000, 0.7)
    return DetectionResult(
        title="Whale Buy Detected" if is_buy else "Whale Sell Detected",
        direction="buy" if is_buy else "sell",
        confidence=confidence,
        reason=f"Single trade {event['size']:.0f} exceeded threshold {threshold:.0f}",
        severity="high" if confidence > 75 else "medium",
        source_label=event["metadata"].get("signal_source", "mock/demo data"),
    )


def volume_spike_detector(volume: float, avg_volume: float, asset: str) -> DetectionResult | None:
    if avg_volume <= 0 or volume / avg_volume < 2:
        return None
    conf = min(95, int((volume / avg_volume) * 30))
    return DetectionResult(
        title="Breakout With Strong Volume",
        direction="long pressure",
        confidence=conf,
        reason=f"Volume spike {volume/avg_volume:.2f}x on {asset}",
        severity="high" if conf > 80 else "medium",
        source_label="volume spike proxy",
    )


def pressure_detector(symbol: str, imbalance: float, regime: str) -> DetectionResult | None:
    if abs(imbalance) < 0.35:
        return None
    long = imbalance > 0
    conf = min(93, int(abs(imbalance) * 100))
    return DetectionResult(
        title="Long Pressure Rising" if long else "Short Pressure Rising",
        direction="long pressure" if long else "short pressure",
        confidence=conf,
        reason=f"Rolling imbalance {imbalance:.2f} in {regime} regime on {symbol}",
        severity="high" if conf > 75 else "medium",
        source_label="futures tape proxy",
    )


def xau_xag_activity_detector(event: dict, regime: str) -> DetectionResult | None:
    if event["symbol"] not in {"XAUUSD", "XAGUSD"}:
        return None
    conf = score_confidence(event["size"], 2.2, 1.0, 200_000, 0.7 if regime != "chop" else 0.4)
    bullish = event["side"] == "buy"
    metal = "Gold" if event["symbol"] == "XAUUSD" else "Silver"
    return DetectionResult(
        title=f"{metal} Aggressive {'Buying' if bullish else 'Selling'} Proxy",
        direction="buy" if bullish else "sell",
        confidence=conf,
        reason=f"Abnormal volume + momentum burst proxy in {regime} regime",
        severity="medium" if conf < 80 else "high",
        source_label="derived signal",
    )
