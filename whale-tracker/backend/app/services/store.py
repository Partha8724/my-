from datetime import datetime

from app.core.config import settings

ASSETS = [
    {"symbol": "BTCUSDT", "asset_type": "crypto", "enabled": True},
    {"symbol": "ETHUSDT", "asset_type": "crypto", "enabled": True},
    {"symbol": "SOLUSDT", "asset_type": "crypto", "enabled": True},
    {"symbol": "XRPUSDT", "asset_type": "crypto", "enabled": True},
    {"symbol": "BNBUSDT", "asset_type": "crypto", "enabled": True},
    {"symbol": "DOGEUSDT", "asset_type": "crypto", "enabled": True},
    {"symbol": "XAUUSD", "asset_type": "metal", "enabled": True},
    {"symbol": "XAGUSD", "asset_type": "metal", "enabled": True},
]

watchlist: list[dict] = []
alerts: list[dict] = []
signals: list[dict] = []
provider_status = [
    {"provider": "mock-demo", "status": "ok", "message": "demo mode", "updated_at": datetime.utcnow().isoformat()},
    {"provider": "binance", "status": "degraded", "message": "configure API/WebSocket", "updated_at": datetime.utcnow().isoformat()},
]
market_cache: dict[str, dict] = {}

admin_settings: dict = {
    "whale_trade_threshold_usd": settings.whale_trade_threshold_usd,
    "volume_multiplier_threshold": settings.volume_multiplier_threshold,
    "confidence_cutoff": settings.confidence_cutoff,
    "symbol_cooldown_seconds": settings.symbol_cooldown_seconds,
    "duplicate_suppression_seconds": settings.duplicate_suppression_seconds,
    "confirmation_window_seconds": settings.confirmation_window_seconds,
    "confirmation_hits": settings.confirmation_hits,
    "asset_enabled": {asset["symbol"]: True for asset in ASSETS},
}
