from collections import defaultdict, deque
from datetime import datetime

from app.signals.detectors import DetectionResult, large_trade_detector, pressure_detector, volume_spike_detector, xau_xag_activity_detector
from app.services.store import admin_settings


class SignalEngine:
    def __init__(self) -> None:
        self.volume_windows: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=60))

    def evaluate_event(self, event: dict, analytics: dict) -> list[DetectionResult]:
        out: list[DetectionResult] = []
        whale_threshold = float(admin_settings["whale_trade_threshold_usd"])
        min_volatility = 0.0008

        if analytics["volatility"] < min_volatility and event["size"] < (whale_threshold * 1.5):
            return out

        trade = large_trade_detector(event, whale_threshold)
        if trade:
            out.append(trade)

        series = self.volume_windows[event["symbol"]]
        size = max(event["size"], 1.0)
        avg = sum(series) / len(series) if series else size
        series.append(size)
        volume_event = volume_spike_detector(size, avg, event["symbol"])
        if volume_event:
            out.append(volume_event)

        pressure = pressure_detector(event["symbol"], analytics["buy_sell_imbalance"], analytics["trend_regime"])
        if pressure:
            out.append(pressure)

        metal = xau_xag_activity_detector(event, analytics["trend_regime"])
        if metal:
            out.append(metal)
        return out


engine = SignalEngine()


def build_signal_card(symbol: str, result: DetectionResult, price: float, analytics: dict) -> dict:
    bias = 1 if result.direction in {"buy", "long pressure"} else -1
    return {
        "asset": symbol,
        "title": result.title,
        "direction": result.direction,
        "confidence": result.confidence,
        "source_label": result.source_label,
        "entry_zone": f"{price*0.998:.2f} - {price*1.002:.2f}",
        "invalidation": f"{price*(0.992 if bias > 0 else 1.008):.2f}",
        "target1": f"{price*(1.006 if bias > 0 else 0.994):.2f}",
        "target2": f"{price*(1.012 if bias > 0 else 0.988):.2f}",
        "risk_note": "Informational only. Not financial advice.",
        "why": result.reason,
        "analytics": analytics,
        "timestamp": datetime.utcnow(),
    }
