from datetime import datetime
from pydantic import BaseModel


class RuleIn(BaseModel):
    name: str
    asset_type: str = "any"
    symbol: str = "*"
    threshold_usd: float = 0
    percent_move: float = 0
    volume_multiple: float = 0
    volatility_threshold: float = 0
    key_levels: list[float] = []
    cooldown_minutes: int = 15
    quiet_hours: list[list[int]] = []
    enabled: bool = True


class RuleOut(RuleIn):
    id: int

    class Config:
        from_attributes = True


class AlertOut(BaseModel):
    id: int
    created_at: datetime
    event_uid: str
    rule_name: str
    message: str
    delivered_telegram: bool
    delivered_email: bool

    class Config:
        from_attributes = True


class EventOut(BaseModel):
    id: int
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

    class Config:
        from_attributes = True
