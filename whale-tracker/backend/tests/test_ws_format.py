from app.utils.normalizer import normalize_event


def test_ws_event_schema():
    item = normalize_event({'symbol': 'BTCUSDT', 'event_type': 'trade', 'side': 'buy', 'size': 1, 'price': 2, 'timestamp': 3}, 'crypto')
    assert set(item.keys()) == {'symbol', 'asset_type', 'event_type', 'side', 'size', 'price', 'timestamp', 'metadata'}
