from datetime import datetime
from pydantic import BaseModel


class WatchlistCreate(BaseModel):
    symbol: str
    whale_threshold: float = 500000
    min_confidence: int = 60
    cooldown_seconds: int = 120
    enabled: bool = True


class LoginRequest(BaseModel):
    username: str
    password: str


class AlertOut(BaseModel):
    id: int
    symbol: str
    direction: str
    confidence: int
    reason: str
    signal_source: str
    severity: str
    timestamp: datetime


class MarketOverviewOut(BaseModel):
    symbol: str
    price: float
    change_24h: float
    volume: float
    pressure: float
