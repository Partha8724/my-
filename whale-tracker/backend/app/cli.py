from app.db.session import Base, engine, SessionLocal
from app.models.entities import Asset, Rule


def demo_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    assets = [
        Asset(asset_id="crypto-btc", asset_type="crypto", symbol="BTC", venue="binance"),
        Asset(asset_id="crypto-eth", asset_type="crypto", symbol="ETH", venue="ethereum"),
        Asset(asset_id="stock-aapl", asset_type="stock", symbol="AAPL", venue="alpaca"),
        Asset(asset_id="metal-xauusd", asset_type="metal", symbol="XAUUSD", venue="twelvedata"),
    ]
    for a in assets:
        if not db.query(Asset).filter_by(asset_id=a.asset_id).first():
            db.add(a)

    rules = [
        Rule(name="crypto_whale_usd", asset_type="crypto", symbol="*", threshold_usd=1_000_000, cooldown_minutes=10),
        Rule(name="stocks_unusual_move", asset_type="stock", symbol="*", percent_move=2.0, volume_multiple=3.0, cooldown_minutes=15),
        Rule(name="xau_breakout", asset_type="metal", symbol="XAUUSD", percent_move=0.5, volatility_threshold=1.0, key_levels=[2300, 2400, 2500], cooldown_minutes=10),
    ]
    for r in rules:
        if not db.query(Rule).filter_by(name=r.name).first():
            db.add(r)
    db.commit()
    db.close()
    print("Seeded assets and rules.")


if __name__ == "__main__":
    demo_seed()
