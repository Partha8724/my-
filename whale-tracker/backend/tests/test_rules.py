from app.signals.detectors import large_trade_detector

def test_large_trade_detector():
    assert large_trade_detector({'event_type':'trade','size':900000}, 500000)
