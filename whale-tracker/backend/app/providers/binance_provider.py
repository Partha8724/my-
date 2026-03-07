from collections.abc import AsyncGenerator

from app.providers.base import BaseOrderFlowProvider


class BinanceProvider(BaseOrderFlowProvider):
    name = "binance"

    async def subscribe_trades(self, symbols: list[str]) -> AsyncGenerator[dict, None]:
        if False:
            yield {}
        return

    async def subscribe_ticker(self, symbols: list[str]) -> AsyncGenerator[dict, None]:
        if False:
            yield {}
        return

    async def fetch_ohlcv(self, symbol: str, timeframe: str = "1m") -> list[dict]:
        return []

    async def health_check(self) -> dict[str, str]:
        return {"provider": self.name, "status": "degraded", "message": "not configured"}
