from app.services.store import watchlist

watchlist.extend([
    {"id": 1, "symbol": "BTCUSDT", "min_confidence": 60, "whale_threshold": 300000, "cooldown_seconds": 120, "enabled": True},
    {"id": 2, "symbol": "XAUUSD", "min_confidence": 55, "whale_threshold": 150000, "cooldown_seconds": 180, "enabled": True},
])
print("Seeded demo watchlist")
