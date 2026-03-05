from datetime import datetime
import ccxt.async_support as ccxt

from app.providers.base import Provider, NormalizedEvent


class CCXTTradeSpikeProvider(Provider):
    name = "ccxt-binance"

    async def fetch_events(self) -> list[NormalizedEvent]:
        exchange = ccxt.binance()
        try:
            trades = await exchange.fetch_trades("BTC/USDT", limit=50)
            if not trades:
                return []
            sizes = [t["amount"] * t["price"] for t in trades if t.get("amount") and t.get("price")]
            avg = sum(sizes) / len(sizes)
            biggest = max(trades, key=lambda t: (t.get("amount", 0) * t.get("price", 0)))
            biggest_usd = biggest["amount"] * biggest["price"]
            if biggest_usd < avg * 3:
                return []
            side = biggest.get("side", "unknown")
            return [
                NormalizedEvent(
                    event_uid=f"ccxt-{biggest['id']}",
                    timestamp=datetime.utcfromtimestamp(biggest["timestamp"] / 1000),
                    asset_symbol="BTC",
                    asset_type="crypto",
                    event_type="large_swap",
                    amount_usd=biggest_usd,
                    direction=side,
                    from_label="binance",
                    to_label="market",
                    tx_hash=None,
                    confidence=0.75,
                    source=self.name,
                    payload={"avg_trade_usd": avg, "price": biggest["price"]},
                )
            ]
        finally:
            await exchange.close()
