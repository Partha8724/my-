from datetime import datetime, timedelta

from app.models.entities import Rule, Event, Alert
from app.rules.engine import should_trigger, dedupe_key
from app.utils import utc_now


def mk_rule(**kwargs):
    base = dict(
        name="r1",
        asset_type="crypto",
        symbol="BTC",
        threshold_usd=1_000_000,
        percent_move=0,
        volume_multiple=0,
        volatility_threshold=0,
        key_levels=[],
        cooldown_minutes=15,
        quiet_hours=[],
        enabled=True,
    )
    base.update(kwargs)
    return Rule(**base)


def mk_event(**kwargs):
    base = dict(
        event_uid="e1",
        timestamp=utc_now(),
        asset_symbol="BTC",
        asset_type="crypto",
        event_type="large_transfer",
        amount_usd=2_000_000,
        direction="in",
        from_label="a",
        to_label="b",
        tx_hash="0x1",
        confidence=0.8,
        source="test",
        payload={"percent_move": 3, "volume_multiple": 4, "volatility": 2, "price": 2400},
    )
    base.update(kwargs)
    return Event(**base)


def test_should_trigger_threshold_passes():
    ok, why = should_trigger(mk_rule(), mk_event())
    assert ok is True
    assert why == "triggered"


def test_should_trigger_cooldown_blocks():
    last = Alert(created_at=utc_now() - timedelta(minutes=1), event_uid="e0", rule_name="r1", dedupe_key="k", message="m")
    ok, why = should_trigger(mk_rule(cooldown_minutes=10), mk_event(), last)
    assert ok is False
    assert why == "cooldown"


def test_dedupe_key_stable_bucket():
    e = mk_event(timestamp=datetime(2025, 1, 1, 12, 3, 0))
    key = dedupe_key(mk_rule(name="test"), e)
    assert key.startswith("test:BTC:large_transfer:")
