import asyncio
from app.providers.factory import get_market_provider
from app.services.state import state
from app.services.ws import manager
from app.alerts.engine import generate_alert_from_event, generate_signal

TRACKED = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT', 'BNBUSDT', 'DOGEUSDT', 'XAUUSD', 'XAGUSD']


async def run_streams():
    provider = get_market_provider()
    health = await provider.health_check()
    state.provider_status[provider.name] = health

    tasks = []
    for symbol in TRACKED:
        tasks.append(asyncio.create_task(_stream_symbol(provider, symbol)))
    await asyncio.gather(*tasks)


async def _stream_symbol(provider, symbol: str):
    async for event in provider.subscribe_trades(symbol):
        state.market_events.appendleft(event)
        side = 1 if event['side'] == 'buy' else -1
        state.pressure[symbol] = max(-100, min(100, state.pressure[symbol] + (event['size'] / 1_000_000) * side))

        alert = generate_alert_from_event(event)
        if alert:
            state.alerts.appendleft(alert)
            signal = generate_signal(alert, event['price'])
            state.signals.appendleft(signal)
            await manager.broadcast({'type': 'alert', 'payload': alert})
            await manager.broadcast({'type': 'signal', 'payload': signal})

        state.latest_ticker[symbol] = {
            'symbol': symbol,
            'price': event['price'],
            'change_24h': round((event['price'] % 10) - 5, 2),
            'volume': event['size'] * 20,
            'pressure': state.pressure[symbol],
        }
        await manager.broadcast({'type': 'ticker', 'payload': state.latest_ticker[symbol]})
