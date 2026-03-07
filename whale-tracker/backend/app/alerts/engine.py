from __future__ import annotations
from datetime import datetime
from app.core.config import settings
from app.signals.detectors import large_trade_detector, confidence_score


def severity_from_confidence(score: int) -> str:
    if score >= 90:
        return 'extreme'
    if score >= 75:
        return 'high'
    if score >= 60:
        return 'medium'
    return 'low'


def generate_alert_from_event(event: dict) -> dict | None:
    if not large_trade_detector(event, settings.whale_trade_threshold):
        return None

    direction = 'buy' if event.get('side') == 'buy' else 'sell'
    conf = confidence_score(
        size=event.get('size', 0),
        volume_mult=2.2,
        trend_alignment=0.5 if direction == 'buy' else -0.5,
        has_oi=event.get('asset_type') == 'crypto',
        has_liq=event.get('asset_type') == 'crypto',
    )
    reason = f"Large {direction} trade exceeded threshold ({event.get('size'):.0f})"
    return {
        'symbol': event['symbol'],
        'direction': direction,
        'confidence': conf,
        'reason': reason,
        'timestamp': datetime.utcnow(),
        'signal_source': event.get('source_label', 'volume spike proxy'),
        'severity': severity_from_confidence(conf),
    }


def generate_signal(alert: dict, price: float) -> dict:
    bullish = alert['direction'] in {'buy', 'long pressure'}
    title = 'Whale Buy Detected' if bullish else 'Whale Sell Detected'
    return {
        'symbol': alert['symbol'],
        'title': title,
        'direction': alert['direction'],
        'confidence': alert['confidence'],
        'data_source_confidence': 'high confidence' if alert['confidence'] >= 80 else 'medium confidence',
        'source_label': 'direct provider signal' if 'exchange' in alert['signal_source'] else 'derived signal',
        'entry_zone': f"{price * (0.998 if bullish else 1.002):.2f} - {price:.2f}",
        'invalidation': f"{price * (0.992 if bullish else 1.008):.2f}",
        'target_1': f"{price * (1.01 if bullish else 0.99):.2f}",
        'target_2': f"{price * (1.02 if bullish else 0.98):.2f}",
        'risk_note': 'Informational alert only; not financial advice.',
        'reason': alert['reason'],
        'timestamp': datetime.utcnow(),
    }
