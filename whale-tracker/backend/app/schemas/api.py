from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AssetOut(BaseModel):
    symbol: str
    asset_type: str
    enabled: bool


class WatchlistCreate(BaseModel):
    symbol: str
    min_confidence: int = 60
    whale_threshold: float = 200000
    cooldown_seconds: int = 120
    enabled: bool = True


class WatchlistOut(WatchlistCreate):
    id: int


class AlertOut(BaseModel):
    id: int
    asset: str
    direction: str
    confidence: int
    reason: str
    signal_source: str = Field(alias="source_label")
    severity: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class SignalOut(BaseModel):
    id: int
    asset: str
    title: str
    direction: str
    confidence: int
    signal_source: str = Field(alias="source_label")
    entry_zone: str
    invalidation: str
    target1: str
    target2: str
    risk_note: str
    why: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class EventEnvelope(BaseModel):
    symbol: str
    asset_type: str
    event_type: str
    side: str
    size: float
    price: float
    timestamp: datetime
    metadata: dict


class SettingsPayload(BaseModel):
    whale_trade_threshold_usd: float
    volume_multiplier_threshold: float
    confidence_cutoff: int
    symbol_cooldown_seconds: int
    duplicate_suppression_seconds: int
    confirmation_window_seconds: int
    confirmation_hits: int
    asset_enabled: dict[str, bool]
