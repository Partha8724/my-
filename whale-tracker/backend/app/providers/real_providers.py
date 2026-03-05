from datetime import datetime
import httpx
from tenacity import retry, wait_exponential, stop_after_attempt

from app.config import settings
from app.providers.base import Provider, NormalizedEvent


class WhaleAlertProvider(Provider):
    name = "whale-alert"

    @retry(wait=wait_exponential(min=1, max=8), stop=stop_after_attempt(3))
    async def fetch_events(self) -> list[NormalizedEvent]:
        if not settings.whale_alert_api_key:
            return []
        url = "https://api.whale-alert.io/v1/transactions"
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params={"api_key": settings.whale_alert_api_key, "min_value": 500000})
            r.raise_for_status()
            data = r.json()
        events = []
        for tx in data.get("transactions", []):
            events.append(
                NormalizedEvent(
                    event_uid=f"whale-{tx.get('id', tx.get('hash'))}",
                    timestamp=datetime.utcfromtimestamp(tx["timestamp"]),
                    asset_symbol=tx.get("symbol", "UNKNOWN").upper(),
                    asset_type="crypto",
                    event_type="large_transfer",
                    amount_usd=float(tx.get("amount_usd") or 0),
                    direction="unknown",
                    from_label=(tx.get("from") or {}).get("owner_type"),
                    to_label=(tx.get("to") or {}).get("owner_type"),
                    tx_hash=tx.get("hash"),
                    confidence=0.85,
                    source=self.name,
                    payload=tx,
                )
            )
        return events


class TwelveDataXAUProvider(Provider):
    name = "twelve-data"

    async def fetch_events(self) -> list[NormalizedEvent]:
        if not settings.twelvedata_api_key:
            return []
        url = "https://api.twelvedata.com/time_series"
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params={"symbol": "XAU/USD", "interval": "1min", "outputsize": 2, "apikey": settings.twelvedata_api_key})
            r.raise_for_status()
            data = r.json()
        vals = data.get("values", [])
        if len(vals) < 2:
            return []
        latest, prev = vals[0], vals[1]
        lp = float(latest["close"])
        pp = float(prev["close"])
        pct = ((lp - pp) / pp) * 100 if pp else 0
        return [
            NormalizedEvent(
                event_uid=f"xau-{latest['datetime']}",
                timestamp=datetime.fromisoformat(latest["datetime"]),
                asset_symbol="XAUUSD",
                asset_type="metal",
                event_type="price_spike",
                amount_usd=None,
                direction="up" if pct >= 0 else "down",
                from_label=None,
                to_label=None,
                tx_hash=None,
                confidence=0.8,
                source=self.name,
                payload={"percent_move": abs(pct), "price": lp, "volatility": abs(pct)},
            )
        ]
