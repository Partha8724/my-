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


class SignalOut(BaseModel):
    symbol: str
    venue: str
    bullish_chance: int
    bearish_chance: int
    signal: str
    whale_direction: str
    total_whale_usd: float
    event_count: int
    alert_count: int
    last_event_type: str
    last_event_at: datetime
    summary: str
    sources: list[str]
    trend: list[float]


class WhaleOrderOut(BaseModel):
    event_uid: str
    symbol: str
    event_type: str
    amount_usd: float
    direction: str
    confidence: float
    source: str
    timestamp: datetime
    from_label: str | None
    to_label: str | None
    bias: str


class AssistantCoinOut(BaseModel):
    symbol: str
    venue: str
    signal: str
    outlook: str
    setup_quality: int
    bullish_chance: int
    bearish_chance: int
    whale_direction: str
    total_whale_usd: float
    event_count: int
    alert_count: int
    price: float | None
    change_24h: float | None
    volume_24h: float | None
    live_supported: bool
    summary: str
    risk_note: str
    sources: list[str]
    trend: list[float]
    last_event_type: str
    last_event_at: datetime


class AssistantBriefOut(BaseModel):
    generated_at: datetime
    market_mode: str
    best_setup: AssistantCoinOut | None
    best_short: AssistantCoinOut | None
    watchlist: list[AssistantCoinOut]
    commentary: list[str]
