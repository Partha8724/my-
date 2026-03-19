from datetime import datetime, timedelta

from app.models.entities import Event
from app.signals.service import (
    build_assistant_brief,
    build_signal_summary,
    build_trend,
    compute_setup_quality,
    event_bias,
    score_event,
)
from app.utils import utc_now


def mk_event(**kwargs):
    base = dict(
        event_uid="signal-e1",
        timestamp=utc_now(),
        asset_symbol="BTC",
        asset_type="crypto",
        event_type="large_swap",
        amount_usd=4_000_000,
        direction="buy",
        from_label="wallet_a",
        to_label="wallet_b",
        tx_hash="0x123",
        confidence=0.9,
        source="test",
        payload={"percent_move": 2.5, "volume_multiple": 4.2, "volatility": 1.8},
    )
    base.update(kwargs)
    return Event(**base)


def test_score_event_rewards_recent_bullish_whale_activity():
    event = mk_event()
    score = score_event(event, utc_now())
    assert score > 20


def test_score_event_penalizes_bearish_exchange_flow():
    event = mk_event(
        event_type="exchange_flow",
        direction="in",
        confidence=0.2,
        amount_usd=100_000,
        payload={},
    )
    score = score_event(event, utc_now())
    assert score < 0


def test_score_event_recency_decay_reduces_signal_strength():
    fresh = mk_event(timestamp=utc_now())
    stale = mk_event(timestamp=utc_now() - timedelta(hours=23))
    assert score_event(fresh, utc_now()) > score_event(stale, utc_now())


def test_build_signal_summary_returns_short_for_low_score():
    signal, summary = build_signal_summary(35, 8, 22)
    assert signal == "SHORT"
    assert "Distribution" in summary


def test_event_bias_marks_exchange_inflow_as_bearish():
    event = mk_event(event_type="exchange_flow", direction="in")
    assert event_bias(event) == "bearish"


def test_build_trend_returns_six_points():
    now = utc_now()
    events = [
      mk_event(timestamp=now - timedelta(minutes=30)),
      mk_event(timestamp=now - timedelta(hours=2, minutes=15), direction="sell"),
    ]
    trend = build_trend(events, now)
    assert len(trend) == 6
    assert all(5 <= point <= 95 for point in trend)


def test_compute_setup_quality_rewards_live_momentum_and_accumulation():
    signal_row = {
        "symbol": "BTC",
        "venue": "binance",
        "bullish_chance": 71,
        "bearish_chance": 29,
        "signal": "LONG",
        "whale_direction": "accumulation",
        "total_whale_usd": 8_000_000,
        "event_count": 3,
        "alert_count": 2,
        "last_event_type": "large_swap",
        "last_event_at": utc_now(),
        "summary": "Whale accumulation and trade activity support upside continuation.",
        "sources": ["ccxt-binance"],
        "trend": [48, 52, 58, 64, 71, 76],
    }
    snapshot = {"price": 102000.0, "change_24h": 5.8, "volume_24h": 2500000000.0, "live_supported": True}

    assert compute_setup_quality(signal_row, snapshot) > signal_row["bullish_chance"]


def test_build_assistant_brief_prefers_long_setup_for_best_setup():
    now = utc_now()
    signal_rows = [
        {
            "symbol": "BTC",
            "venue": "binance",
            "bullish_chance": 74,
            "bearish_chance": 26,
            "signal": "LONG",
            "whale_direction": "accumulation",
            "total_whale_usd": 9_000_000,
            "event_count": 4,
            "alert_count": 2,
            "last_event_type": "large_swap",
            "last_event_at": now,
            "summary": "Bullish setup",
            "sources": ["ccxt-binance"],
            "trend": [45, 50, 56, 63, 69, 75],
        },
        {
            "symbol": "ETH",
            "venue": "binance",
            "bullish_chance": 33,
            "bearish_chance": 67,
            "signal": "SHORT",
            "whale_direction": "distribution",
            "total_whale_usd": 4_000_000,
            "event_count": 2,
            "alert_count": 1,
            "last_event_type": "exchange_flow",
            "last_event_at": now,
            "summary": "Bearish setup",
            "sources": ["mock-crypto"],
            "trend": [59, 54, 49, 44, 41, 35],
        },
    ]
    snapshots = {
        "BTC": {"price": 101500.0, "change_24h": 3.4, "volume_24h": 1800000000.0, "live_supported": True},
        "ETH": {"price": 3200.0, "change_24h": -4.1, "volume_24h": 800000000.0, "live_supported": True},
    }

    brief = build_assistant_brief(signal_rows, snapshots)

    assert brief["best_setup"]["symbol"] == "BTC"
    assert brief["best_short"]["symbol"] == "ETH"
    assert brief["market_mode"] == "live"
