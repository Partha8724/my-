from app.alerts.engine import generate_alert_from_event
from app.signals.detectors import confidence_score
from app.utils.normalizer import normalize_event


def test_alert_threshold():
    event = {'symbol': 'BTCUSDT', 'event_type': 'trade', 'size': 900000, 'side': 'buy', 'price': 62000, 'asset_type': 'crypto', 'source_label': 'confirmed trade flow'}
    alert = generate_alert_from_event(event)
    assert alert is not None
    assert alert['confidence'] >= 50


def test_confidence_score_range():
    score = confidence_score(600000, 2.3, 0.8, True, True)
    assert 0 <= score <= 100


def test_normalization():
    normalized = normalize_event({'symbol': 'XAUUSD', 'size': '1200', 'price': '2360.2', 'timestamp': 1}, 'metal')
    assert normalized['asset_type'] == 'metal'
    assert normalized['size'] == 1200.0
