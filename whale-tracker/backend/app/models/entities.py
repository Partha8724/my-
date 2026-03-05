from datetime import datetime
from sqlalchemy import String, Float, DateTime, JSON, UniqueConstraint, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    asset_type: Mapped[str] = mapped_column(String(32), index=True)
    symbol: Mapped[str] = mapped_column(String(32), index=True)
    venue: Mapped[str] = mapped_column(String(64), default="default")
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (UniqueConstraint("event_uid", name="uq_event_uid"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_uid: Mapped[str] = mapped_column(String(128), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    asset_symbol: Mapped[str] = mapped_column(String(32), index=True)
    asset_type: Mapped[str] = mapped_column(String(32), index=True)
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    amount_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    direction: Mapped[str | None] = mapped_column(String(16), nullable=True)
    from_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    to_label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    tx_hash: Mapped[str | None] = mapped_column(String(256), nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    source: Mapped[str] = mapped_column(String(64))
    payload: Mapped[dict] = mapped_column(JSON, default={})


class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    asset_type: Mapped[str] = mapped_column(String(32), default="any")
    symbol: Mapped[str] = mapped_column(String(32), default="*")
    threshold_usd: Mapped[float] = mapped_column(Float, default=0)
    percent_move: Mapped[float] = mapped_column(Float, default=0)
    volume_multiple: Mapped[float] = mapped_column(Float, default=0)
    volatility_threshold: Mapped[float] = mapped_column(Float, default=0)
    key_levels: Mapped[list] = mapped_column(JSON, default=[])
    cooldown_minutes: Mapped[int] = mapped_column(Integer, default=15)
    quiet_hours: Mapped[list] = mapped_column(JSON, default=[])
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class Alert(Base):
    __tablename__ = "alerts"
    __table_args__ = (UniqueConstraint("dedupe_key", name="uq_alert_dedupe_key"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    event_uid: Mapped[str] = mapped_column(String(128), index=True)
    rule_name: Mapped[str] = mapped_column(String(128))
    dedupe_key: Mapped[str] = mapped_column(String(256), index=True)
    message: Mapped[str] = mapped_column(String(1024))
    delivered_telegram: Mapped[bool] = mapped_column(Boolean, default=False)
    delivered_email: Mapped[bool] = mapped_column(Boolean, default=False)
