from dataclasses import dataclass
from datetime import datetime


@dataclass
class NormalizedEvent:
    event_uid: str
    timestamp: datetime
    asset_symbol: str
    asset_type: str
    event_type: str
    amount_usd: float | None
    direction: str | None
    from_label: str | None
    to_label: str | None
    tx_hash: str | None
    confidence: float
    source: str
    payload: dict


class Provider:
    name = "base"

    async def fetch_events(self) -> list[NormalizedEvent]:
        raise NotImplementedError
