from __future__ import annotations
from collections import defaultdict, deque
from threading import Lock


class RuntimeState:
    def __init__(self):
        self.lock = Lock()
        self.latest_ticker: dict[str, dict] = {}
        self.alerts: deque[dict] = deque(maxlen=500)
        self.signals: deque[dict] = deque(maxlen=500)
        self.market_events: deque[dict] = deque(maxlen=2000)
        self.provider_status: dict[str, dict] = {}
        self.watchlist: dict[str, dict] = {}
        self.pressure: dict[str, float] = defaultdict(float)


state = RuntimeState()
