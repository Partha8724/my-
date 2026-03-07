from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.core.security import create_access_token, verify_password, hash_password, decode_access_token
from app.schemas.api import LoginRequest, WatchlistCreate
from app.services.state import state
from app.services.ws import manager

router = APIRouter()
auth_scheme = HTTPBearer(auto_error=False)


def get_current_user(creds: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if not creds:
        raise HTTPException(status_code=401, detail='Missing token')
    subject = decode_access_token(creds.credentials)
    if not subject:
        raise HTTPException(status_code=401, detail='Invalid token')
    return subject


@router.get('/health')
async def health():
    return {'status': 'ok', 'time': datetime.utcnow().isoformat(), 'demo_mode': settings.demo_mode}


@router.post('/api/auth/login')
async def login(payload: LoginRequest):
    if payload.username != settings.admin_username or not verify_password(payload.password, hash_password(settings.admin_password)):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return {'access_token': create_access_token(payload.username), 'token_type': 'bearer'}


@router.get('/api/assets')
async def get_assets():
    return [
        {'symbol': 'BTCUSDT', 'asset_type': 'crypto'},
        {'symbol': 'ETHUSDT', 'asset_type': 'crypto'},
        {'symbol': 'SOLUSDT', 'asset_type': 'crypto'},
        {'symbol': 'XRPUSDT', 'asset_type': 'crypto'},
        {'symbol': 'BNBUSDT', 'asset_type': 'crypto'},
        {'symbol': 'DOGEUSDT', 'asset_type': 'crypto'},
        {'symbol': 'XAUUSD', 'asset_type': 'metal'},
        {'symbol': 'XAGUSD', 'asset_type': 'metal'},
    ]


@router.get('/api/watchlist')
async def get_watchlist():
    return list(state.watchlist.values())


@router.post('/api/watchlist')
async def add_watchlist(item: WatchlistCreate, _user: str = Depends(get_current_user)):
    state.watchlist[item.symbol] = item.model_dump()
    return item


@router.delete('/api/watchlist/{symbol}')
async def delete_watchlist(symbol: str, _user: str = Depends(get_current_user)):
    state.watchlist.pop(symbol, None)
    return {'deleted': symbol}


@router.get('/api/alerts')
async def get_alerts():
    return list(state.alerts)


@router.get('/api/alerts/export.csv')
async def export_alerts_csv():
    rows = ['symbol,direction,confidence,reason,severity,timestamp']
    for a in state.alerts:
        rows.append(f"{a['symbol']},{a['direction']},{a['confidence']},\"{a['reason']}\",{a['severity']},{a['timestamp']}")
    return {'csv': '\n'.join(rows)}


@router.get('/api/signals')
async def get_signals():
    return list(state.signals)


@router.get('/api/providers/status')
async def provider_status():
    return list(state.provider_status.values())


@router.get('/api/market/overview')
async def market_overview():
    return list(state.latest_ticker.values())


@router.get('/api/market/{symbol}')
async def market_symbol(symbol: str):
    return state.latest_ticker.get(symbol, {'symbol': symbol, 'price': 0, 'change_24h': 0, 'volume': 0, 'pressure': 0})


@router.get('/api/market/{symbol}/history')
async def market_history(symbol: str, timeframe: str = '1m'):
    events = [e for e in state.market_events if e['symbol'] == symbol][:100]
    return {'symbol': symbol, 'timeframe': timeframe, 'events': events}


@router.get('/api/settings')
async def get_settings():
    return {
        'whale_threshold': settings.whale_trade_threshold,
        'volume_multiplier_threshold': settings.volume_multiplier_threshold,
        'confidence_cutoff': settings.confidence_cutoff,
        'demo_mode': settings.demo_mode,
    }


@router.websocket('/ws/stream')
async def websocket_stream(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        manager.disconnect(websocket)
