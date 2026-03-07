
def normalize_event(event: dict, asset_type: str) -> dict:
    return {
        'symbol': event.get('symbol'),
        'asset_type': asset_type,
        'event_type': event.get('event_type', 'trade'),
        'side': event.get('side', 'neutral'),
        'size': float(event.get('size', 0)),
        'price': float(event.get('price', 0)),
        'timestamp': event.get('timestamp'),
        'metadata': event.get('metadata', {}),
    }
