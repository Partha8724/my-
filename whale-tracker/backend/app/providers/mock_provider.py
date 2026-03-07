import asyncio
import random
from collections.abc import AsyncGenerator
from datetime import datetime

from app.providers.base import BaseOrderFlowProvider


class MockUnifiedProvider(BaseOrderFlowProvider):
    name = "mock-demo"

    def __init__(self) -> None:
        self.tick = 0
        self.regime = {"XAUUSD": "balance", "XAGUSD": "balance"}

    async def subscribe_trades(self, symbols: list[str]) -> AsyncGenerator[dict, None]:
        while True:
            self.tick += 1
            symbol = random.choice(symbols)
            if self.tick % 55 == 0:
                symbol = random.choice(["XAUUSD", "XAGUSD"])
                self.regime[symbol] = random.choice(["accumulation", "distribution", "balance"])

            base_price = {"BTCUSDT": 68000, "ETHUSDT": 3500, "SOLUSDT": 145, "XRPUSDT": 0.62, "BNBUSDT": 620, "DOGEUSDT": 0.18, "XAUUSD": 1980, "XAGUSD": 24}.get(symbol, 100)
            side = random.choice(["buy", "sell"])

            burst = self.tick % 40 in {0, 1, 2, 3}
            periodic_spike = self.tick % 30 == 0
            if burst:
                size = random.uniform(500_000, 1_800_000)
            elif periodic_spike:
                size = random.uniform(300_000, 900_000)
            else:
                size = random.uniform(8_000, 220_000)

            if symbol in {"XAUUSD", "XAGUSD"} and self.regime[symbol] == "accumulation":
                side = "buy" if random.random() > 0.25 else "sell"
            if symbol in {"XAUUSD", "XAGUSD"} and self.regime[symbol] == "distribution":
                side = "sell" if random.random() > 0.25 else "buy"

            drift = 1.8 if side == "buy" else -1.8
            if symbol in {"XAUUSD", "XAGUSD"}:
                drift *= 0.4

            event = {
                "symbol": symbol,
                "asset_type": "crypto" if "USDT" in symbol else "metal",
                "event_type": "trade",
                "side": side,
                "size": size,
                "price": max(0.0001, base_price + random.uniform(-0.9, 0.9) + drift),
                "timestamp": datetime.utcnow(),
                "metadata": {
                    "signal_source": random.choice([
                        "confirmed trade flow",
                        "exchange liquidation/open interest data",
                        "volume spike proxy",
                        "futures tape proxy",
                        "mock/demo data",
                    ]),
                    "provider": self.name,
                    "burst": burst,
                    "periodic_spike": periodic_spike,
                    "metal_regime": self.regime.get(symbol),
                },
            }
            yield event
            await asyncio.sleep(0.55)

    async def subscribe_ticker(self, symbols: list[str]) -> AsyncGenerator[dict, None]:
        while True:
            symbol = random.choice(symbols)
            yield {
                "symbol": symbol,
                "event_type": "ticker",
                "price": random.uniform(10, 70000),
                "change_24h": random.uniform(-5, 5),
                "volume": random.uniform(1_000_000, 9_000_000_000),
                "timestamp": datetime.utcnow(),
            }
            await asyncio.sleep(1.2)

    async def fetch_ohlcv(self, symbol: str, timeframe: str = "1m") -> list[dict]:
        now = datetime.utcnow()
        data = []
        p = 100
        for i in range(80):
            p = p + random.uniform(-1, 1)
            data.append({"t": now.timestamp() - (79 - i) * 60, "o": p - 0.3, "h": p + 0.8, "l": p - 1, "c": p, "v": random.uniform(1000, 5000)})
        return data

    async def fetch_open_interest(self, symbol: str) -> dict | None:
        return {"symbol": symbol, "oi": random.uniform(100_000, 2_000_000), "change_pct": random.uniform(-10, 10)}

    async def fetch_liquidations(self, symbol: str) -> dict | None:
        return {"symbol": symbol, "buy_liq": random.uniform(0, 5_000_000), "sell_liq": random.uniform(0, 5_000_000)}

    async def health_check(self) -> dict[str, str]:
        return {"provider": self.name, "status": "ok", "message": "demo mode"}
