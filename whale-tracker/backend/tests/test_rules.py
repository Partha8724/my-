from datetime import datetime, timedelta

from app.services.alert_policy import AlertPolicy
from app.services.analytics import analytics_engine
from app.services.engine import engine


def test_large_trade_signal_generation():
    event = {
        "symbol": "BTCUSDT",
        "asset_type": "crypto",
        "event_type": "trade",
        "side": "buy",
        "size": 1_500_000,
        "price": 67000,
        "metadata": {"signal_source": "confirmed trade flow"},
    }
    analytics = analytics_engine.update("BTCUSDT", "buy", 1_500_000, 67000, datetime.utcnow())
    analytics["volatility"] = 0.01
    res = engine.evaluate_event(event, analytics)
    assert any("Whale" in r.title for r in res)


def test_xau_proxy_generation():
    event = {
        "symbol": "XAUUSD",
        "asset_type": "metal",
        "event_type": "trade",
        "side": "sell",
        "size": 600000,
        "price": 1990,
        "metadata": {"signal_source": "derived signal"},
    }
    analytics = analytics_engine.update("XAUUSD", "sell", 600000, 1990, datetime.utcnow())
    analytics["volatility"] = 0.01
    res = engine.evaluate_event(event, analytics)
    assert any("Gold" in r.title for r in res)


def test_alert_policy_confirmation_and_cooldown():
    policy = AlertPolicy()
    now = datetime.utcnow()
    ok, _ = policy.should_emit("BTCUSDT", "sig", 90, now)
    assert not ok
    ok, _ = policy.should_emit("BTCUSDT", "sig", 90, now + timedelta(seconds=2))
    assert ok
    ok, reason = policy.should_emit("BTCUSDT", "sig2", 90, now + timedelta(seconds=5))
    assert not ok and reason == "symbol cooldown"
