from datetime import datetime

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from app.core.config import settings
from app.schemas.api import LoginRequest, SettingsPayload, TokenOut, WatchlistCreate
from app.services.realtime import manager
from app.services.store import ASSETS, admin_settings, alerts, market_cache, provider_status, signals, watchlist
from app.utils.security import create_access_token

router = APIRouter()


@router.get("/health")
def health():
    provider_ok = any(p["status"] == "ok" for p in provider_status)
    return {
        "status": "ok" if provider_ok else "degraded",
        "app": settings.app_name,
        "demo_mode": settings.demo_mode,
        "env": settings.env,
        "providers": provider_status,
    }


@router.post("/api/auth/login", response_model=TokenOut)
def login(payload: LoginRequest):
    if payload.username != settings.admin_username or payload.password != settings.admin_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": payload.username})
    return TokenOut(access_token=token)


@router.get("/api/assets")
def get_assets():
    assets = []
    enabled_map = admin_settings.get("asset_enabled", {})
    for asset in ASSETS:
        assets.append({**asset, "enabled": enabled_map.get(asset["symbol"], asset.get("enabled", True))})
    return assets


@router.get("/api/settings", response_model=SettingsPayload)
def get_settings():
    return admin_settings


@router.put("/api/settings", response_model=SettingsPayload)
def update_settings(payload: SettingsPayload):
    admin_settings.update(payload.model_dump())
    return admin_settings


@router.get("/api/watchlist")
def get_watchlist():
    return watchlist


@router.post("/api/watchlist")
def add_watchlist(item: WatchlistCreate):
    record = item.model_dump()
    record["id"] = len(watchlist) + 1
    watchlist.append(record)
    return record


@router.delete("/api/watchlist/{item_id}")
def remove_watchlist(item_id: int):
    idx = next((i for i, x in enumerate(watchlist) if x["id"] == item_id), None)
    if idx is None:
        raise HTTPException(404, "Watchlist item not found")
    return watchlist.pop(idx)


@router.get("/api/alerts")
def get_alerts(limit: int = 200):
    return list(reversed(alerts[-limit:]))


@router.get("/api/alerts/export.csv")
def export_alerts_csv():
    rows = ["asset,direction,confidence,reason,timestamp,source,severity"]
    for a in alerts:
        rows.append(f"{a['asset']},{a['direction']},{a['confidence']},\"{a['reason']}\",{a['timestamp']},{a['source_label']},{a['severity']}")
    return "\n".join(rows)


@router.get("/api/signals")
def get_signals(limit: int = 200):
    return list(reversed(signals[-limit:]))


@router.get("/api/providers/status")
def provider_health():
    return provider_status


@router.get("/api/market/overview")
def market_overview():
    values = list(market_cache.values())
    top_movers = sorted(values, key=lambda x: abs(x.get("analytics", {}).get("buy_sell_imbalance", 0)), reverse=True)[:5]
    heatmap = [
        {
            "symbol": x.get("symbol"),
            "score": round(x.get("analytics", {}).get("buy_sell_imbalance", 0) * 100, 2),
            "regime": x.get("analytics", {}).get("trend_regime", "chop"),
        }
        for x in values
    ]
    return {
        "demo_mode": settings.demo_mode,
        "provider_status": provider_status,
        "total_active_alerts": len(alerts),
        "latest_signals": list(reversed(signals[-6:])),
        "market": market_cache,
        "top_movers": top_movers,
        "heatmap": heatmap,
        "updated_at": datetime.utcnow().isoformat(),
    }


@router.get("/api/market/{symbol}")
def market_symbol(symbol: str):
    return market_cache.get(symbol.upper(), {})


@router.get("/api/market/{symbol}/history")
def market_history(symbol: str, timeframe: str = "1m"):
    return {"symbol": symbol.upper(), "timeframe": timeframe, "candles": market_cache.get(symbol.upper(), {}).get("history", [])}


@router.websocket("/ws/stream")
async def ws_stream(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)
