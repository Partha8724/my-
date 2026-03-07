from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any


class BaseMarketDataProvider(ABC):
    name: str

    @abstractmethod
    async def subscribe_trades(self, symbols: list[str]) -> AsyncGenerator[dict[str, Any], None]:
        raise NotImplementedError

    @abstractmethod
    async def subscribe_ticker(self, symbols: list[str]) -> AsyncGenerator[dict[str, Any], None]:
        raise NotImplementedError

    @abstractmethod
    async def fetch_ohlcv(self, symbol: str, timeframe: str = "1m") -> list[dict[str, Any]]:
        raise NotImplementedError

    async def fetch_open_interest(self, symbol: str) -> dict[str, Any] | None:
        return None

    async def fetch_liquidations(self, symbol: str) -> dict[str, Any] | None:
        return None

    @abstractmethod
    async def health_check(self) -> dict[str, str]:
        raise NotImplementedError


class BaseOrderFlowProvider(BaseMarketDataProvider):
    pass


class BaseAlertProvider(ABC):
    @abstractmethod
    async def send(self, payload: dict[str, Any]) -> None:
        raise NotImplementedError
