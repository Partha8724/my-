import random
from datetime import datetime

from app.providers.base import Provider, NormalizedEvent


class MockCryptoProvider(Provider):
    name = "mock-crypto"

    async def fetch_events(self) -> list[NormalizedEvent]:
        now = datetime.utcnow()
        amount = random.uniform(200_000, 5_000_000)
        return [
            NormalizedEvent(
                event_uid=f"mock-crypto-{int(now.timestamp())}",
                timestamp=now,
                asset_symbol=random.choice(["BTC", "ETH"]),
                asset_type="crypto",
                event_type=random.choice(["large_transfer", "exchange_flow", "large_swap"]),
                amount_usd=amount,
                direction=random.choice(["in", "out", "unknown"]),
                from_label="wallet_a",
                to_label="exchange_x",
                tx_hash=f"0x{int(amount)}",
                confidence=0.65,
                source=self.name,
                payload={"note": "mock event"},
            )
        ]


class MockStockProvider(Provider):
    name = "mock-stocks"

    async def fetch_events(self) -> list[NormalizedEvent]:
        now = datetime.utcnow()
        pct = random.uniform(0.5, 6.0)
        volume = random.uniform(2.0, 10.0)
        return [
            NormalizedEvent(
                event_uid=f"mock-stock-{int(now.timestamp())}",
                timestamp=now,
                asset_symbol=random.choice(["AAPL", "TSLA", "NVDA"]),
                asset_type="stock",
                event_type="unusual_volume",
                amount_usd=random.uniform(100_000, 2_000_000),
                direction="up" if pct > 0 else "down",
                from_label=None,
                to_label=None,
                tx_hash=None,
                confidence=0.6,
                source=self.name,
                payload={"percent_move": pct, "volume_multiple": volume, "volatility": random.uniform(1.0, 4.0), "price": random.uniform(100, 300)},
            )
        ]


class MockXAUProvider(Provider):
    name = "mock-xau"

    async def fetch_events(self) -> list[NormalizedEvent]:
        now = datetime.utcnow()
        price = random.uniform(2100, 2600)
        return [
            NormalizedEvent(
                event_uid=f"mock-xau-{int(now.timestamp())}",
                timestamp=now,
                asset_symbol="XAUUSD",
                asset_type="metal",
                event_type="price_spike",
                amount_usd=None,
                direction=random.choice(["up", "down"]),
                from_label=None,
                to_label=None,
                tx_hash=None,
                confidence=0.7,
                source=self.name,
                payload={"percent_move": random.uniform(0.2, 2.0), "volatility": random.uniform(0.5, 3.0), "price": price},
            )
        ]
