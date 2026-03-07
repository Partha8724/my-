from datetime import datetime
from sqlalchemy import String, Float, Integer, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class Asset(Base):
    __tablename__ = 'assets'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    asset_type: Mapped[str] = mapped_column(String(20))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class WatchlistItem(Base):
    __tablename__ = 'watchlist_items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    whale_threshold: Mapped[float] = mapped_column(Float, default=500000)
    min_confidence: Mapped[int] = mapped_column(Integer, default=60)
    cooldown_seconds: Mapped[int] = mapped_column(Integer, default=120)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class MarketEvent(Base):
    __tablename__ = 'market_events'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    asset_type: Mapped[str] = mapped_column(String(20))
    event_type: Mapped[str] = mapped_column(String(50))
    side: Mapped[str] = mapped_column(String(20), default='neutral')
    size: Mapped[float] = mapped_column(Float, default=0)
    price: Mapped[float] = mapped_column(Float, default=0)
    source_label: Mapped[str] = mapped_column(String(50), default='mock/demo data')
    event_metadata: Mapped[dict] = mapped_column("metadata", JSON, default={})
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = 'alerts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    direction: Mapped[str] = mapped_column(String(30))
    confidence: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(String(255))
    signal_source: Mapped[str] = mapped_column(String(80))
    severity: Mapped[str] = mapped_column(String(20))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Signal(Base):
    __tablename__ = 'signals'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    title: Mapped[str] = mapped_column(String(120))
    direction: Mapped[str] = mapped_column(String(30))
    confidence: Mapped[int] = mapped_column(Integer)
    data_source_confidence: Mapped[str] = mapped_column(String(20), default='medium confidence')
    source_label: Mapped[str] = mapped_column(String(50), default='derived signal')
    entry_zone: Mapped[str] = mapped_column(String(60))
    invalidation: Mapped[str] = mapped_column(String(60))
    target_1: Mapped[str] = mapped_column(String(60))
    target_2: Mapped[str] = mapped_column(String(60))
    risk_note: Mapped[str] = mapped_column(String(255))
    reason: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))


class ProviderStatus(Base):
    __tablename__ = 'provider_status'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider_name: Mapped[str] = mapped_column(String(50), unique=True)
    healthy: Mapped[bool] = mapped_column(Boolean, default=True)
    mode: Mapped[str] = mapped_column(String(20), default='demo')
    message: Mapped[str] = mapped_column(String(255), default='ok')
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class NotificationConfig(Base):
    __tablename__ = 'notification_configs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    telegram_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    email_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    webhook_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    browser_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    sound_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    webhook_url: Mapped[str] = mapped_column(String(255), default='')
