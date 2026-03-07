from collections import defaultdict, deque
from datetime import datetime, timedelta
from statistics import pstdev


class AnalyticsEngine:
    def __init__(self) -> None:
        self.trade_windows: dict[str, deque[dict]] = defaultdict(lambda: deque(maxlen=500))

    def update(self, symbol: str, side: str, size: float, price: float, timestamp: datetime) -> dict:
        window = self.trade_windows[symbol]
        window.append({"side": side, "size": size, "price": price, "ts": timestamp})
        cutoff = timestamp - timedelta(minutes=15)
        while window and window[0]["ts"] < cutoff:
            window.popleft()

        buy = sum(x["size"] for x in window if x["side"] == "buy")
        sell = sum(x["size"] for x in window if x["side"] == "sell")
        total = max(buy + sell, 1.0)
        imbalance = (buy - sell) / total
        cumulative_delta = buy - sell

        prices = [x["price"] for x in window][-60:]
        returns = []
        for i in range(1, len(prices)):
            prev = prices[i - 1] if prices[i - 1] else 1
            returns.append((prices[i] - prev) / prev)
        volatility = pstdev(returns) if len(returns) >= 2 else 0.0

        regime = "chop"
        if len(prices) > 10:
            slope = (prices[-1] - prices[0]) / max(abs(prices[0]), 1.0)
            if slope > 0.002:
                regime = "bull"
            elif slope < -0.002:
                regime = "bear"

        return {
            "buy_sell_imbalance": imbalance,
            "cumulative_delta": cumulative_delta,
            "volatility": volatility,
            "trend_regime": regime,
            "buy_volume": buy,
            "sell_volume": sell,
        }


analytics_engine = AnalyticsEngine()
