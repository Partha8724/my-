from __future__ import annotations
import asyncio
import random
import time
from collections.abc import AsyncGenerator
from app.providers.base import BaseMarketDataProvider


class MockProvider(BaseMarketDataProvider):
    name = 'mock-provider'

    def __init__(self):
        self.base_prices = {
            'BTCUSDT': 65000,
            'ETHUSDT': 3200,
            'SOLUSDT': 140,
            'XRPUSDT': 0.58,
            'BNBUSDT': 590,
            'DOGEUSDT': 0.12,
            'XAUUSD': 2360,
            'XAGUSD': 29,
        }

    async def subscribe_trades(self, symbol: str) -> AsyncGenerator[dict, None]:
        while True:
            await asyncio.sleep(1)
            base = self.base_prices.get(symbol, 100)
            price = base * (1 + random.uniform(-0.002, 0.002))
            size = random.uniform(10000, 1200000)
            yield {
                'symbol': symbol,
                'asset_type': 'crypto' if symbol.endswith('USDT') else 'metal',
                'event_type': 'trade',
                'side': 'buy' if random.random() > 0.5 else 'sell',
                'size': round(size, 2),
                'price': round(price, 4),
                'timestamp': int(time.time() * 1000),
                'metadata': {'data_source_confidence': 'medium confidence'},
                'source_label': 'mock/demo data',
            }

    async def subscribe_ticker(self, symbol: str) -> AsyncGenerator[dict, None]:
        while True:
            await asyncio.sleep(2)
            base = self.base_prices.get(symbol, 100)
            price = base * (1 + random.uniform(-0.01, 0.01))
            yield {'symbol': symbol, 'price': round(price, 4), 'change_24h': round(random.uniform(-5, 5), 2), 'volume': random.uniform(1e6, 1e9)}

    async def fetch_ohlcv(self, symbol: str, timeframe: str = '1m', limit: int = 100) -> list[dict]:
        base = self.base_prices.get(symbol, 100)
        ohlcv = []
        for _ in range(limit):
            open_p = base * (1 + random.uniform(-0.01, 0.01))
            close_p = open_p * (1 + random.uniform(-0.005, 0.005))
            high = max(open_p, close_p) * (1 + random.uniform(0, 0.003))
            low = min(open_p, close_p) * (1 - random.uniform(0, 0.003))
            ohlcv.append({'open': open_p, 'high': high, 'low': low, 'close': close_p, 'volume': random.uniform(5000, 50000)})
        return ohlcv

    async def fetch_open_interest(self, symbol: str) -> dict | None:
        if symbol.endswith('USDT'):
            return {'symbol': symbol, 'open_interest': random.uniform(1e7, 9e8), 'source_label': 'exchange liquidation/open interest data'}
        return None

    async def fetch_liquidations(self, symbol: str) -> list[dict] | None:
        if symbol.endswith('USDT'):
            return [{'symbol': symbol, 'size': random.uniform(1e5, 4e6), 'side': 'long' if random.random() > 0.5 else 'short'}]
        return None

    async def health_check(self) -> dict:
        return {'provider': self.name, 'healthy': True, 'mode': 'demo', 'message': 'synthetic stream active'}
