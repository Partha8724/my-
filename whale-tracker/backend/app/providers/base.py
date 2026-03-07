from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator


class BaseMarketDataProvider(ABC):
    name: str = 'base'

    @abstractmethod
    async def subscribe_trades(self, symbol: str) -> AsyncGenerator[dict, None]: ...

    @abstractmethod
    async def subscribe_ticker(self, symbol: str) -> AsyncGenerator[dict, None]: ...

    @abstractmethod
    async def fetch_ohlcv(self, symbol: str, timeframe: str = '1m', limit: int = 100) -> list[dict]: ...

    async def fetch_open_interest(self, symbol: str) -> dict | None:
        return None

    async def fetch_liquidations(self, symbol: str) -> list[dict] | None:
        return None

    @abstractmethod
    async def health_check(self) -> dict: ...
