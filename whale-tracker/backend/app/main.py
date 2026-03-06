from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db.session import Base, engine, get_db
from sqlalchemy import func, case

from app.models.entities import Alert, Rule, Asset, Event
from app.schemas.api import RuleIn, RuleOut, AlertOut, EventOut
from app.workers.ingestion import ingestion_service

app = FastAPI(title="Whale Tracker & Cross-Asset Alert")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    ingestion_service.start()


@app.on_event("shutdown")
def shutdown():
    ingestion_service.stop()


@app.get("/health")
def health():
    return {"status": "ok", "last_run": ingestion_service.last_run, "last_error": ingestion_service.last_error}


@app.get("/alerts", response_model=list[AlertOut])
def alerts(asset: str | None = None, event_type: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Alert).order_by(Alert.created_at.desc())
    if asset:
        q = q.filter(Alert.message.ilike(f"%{asset}%"))
    if event_type:
        q = q.filter(Alert.message.ilike(f"%{event_type}%"))
    return q.limit(200).all()


@app.get("/rules", response_model=list[RuleOut])
def list_rules(db: Session = Depends(get_db)):
    return db.query(Rule).order_by(Rule.id.desc()).all()


@app.post("/rules", response_model=RuleOut)
def create_rule(payload: RuleIn, db: Session = Depends(get_db)):
    rule = Rule(**payload.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


@app.get("/events", response_model=list[EventOut])
def events(limit: int = 200, db: Session = Depends(get_db)):
    max_limit = min(max(limit, 1), 500)
    return db.query(Event).order_by(Event.timestamp.desc()).limit(max_limit).all()


@app.get("/metrics/live")
def live_metrics(minutes: int = 60, db: Session = Depends(get_db)):
    lookback_minutes = min(max(minutes, 1), 24 * 60)
    since = func.datetime("now", f"-{lookback_minutes} minutes")

    recent_events = db.query(Event).filter(Event.timestamp >= since).all()

    total_notional = sum((e.amount_usd or 0) for e in recent_events)
    buy_notional = sum((e.amount_usd or 0) for e in recent_events if (e.direction or "").lower() in {"buy", "in", "up"})
    sell_notional = sum((e.amount_usd or 0) for e in recent_events if (e.direction or "").lower() in {"sell", "out", "down"})

    exposure = {
        "long_notional": buy_notional,
        "short_notional": sell_notional,
        "buy_count": sum(1 for e in recent_events if (e.direction or "").lower() in {"buy", "in", "up"}),
        "sell_count": sum(1 for e in recent_events if (e.direction or "").lower() in {"sell", "out", "down"}),
    }

    assets = []
    asset_rows = (
        db.query(
            Event.asset_symbol.label("asset"),
            Event.asset_type.label("asset_type"),
            func.count(Event.id).label("trade_count"),
            func.sum(func.coalesce(Event.amount_usd, 0)).label("volume_usd"),
            func.sum(case((Event.direction.in_(["buy", "in", "up"]), func.coalesce(Event.amount_usd, 0)), else_=0)).label("buy_usd"),
            func.sum(case((Event.direction.in_(["sell", "out", "down"]), func.coalesce(Event.amount_usd, 0)), else_=0)).label("sell_usd"),
        )
        .filter(Event.timestamp >= since)
        .group_by(Event.asset_symbol, Event.asset_type)
        .order_by(func.sum(func.coalesce(Event.amount_usd, 0)).desc())
        .limit(20)
        .all()
    )
    for row in asset_rows:
        assets.append({
            "asset": row.asset,
            "asset_type": row.asset_type,
            "trade_count": row.trade_count,
            "volume_usd": float(row.volume_usd or 0),
            "buy_usd": float(row.buy_usd or 0),
            "sell_usd": float(row.sell_usd or 0),
            "net_usd": float((row.buy_usd or 0) - (row.sell_usd or 0)),
        })

    whale_wallets = []
    wallet_rows = (
        db.query(
            Event.from_label.label("wallet"),
            func.count(Event.id).label("activity_count"),
            func.sum(func.coalesce(Event.amount_usd, 0)).label("volume_usd"),
            func.max(Event.timestamp).label("last_seen"),
        )
        .filter(Event.timestamp >= since)
        .filter(Event.from_label.isnot(None))
        .group_by(Event.from_label)
        .order_by(func.sum(func.coalesce(Event.amount_usd, 0)).desc())
        .limit(15)
        .all()
    )
    for row in wallet_rows:
        whale_wallets.append({
            "wallet": row.wallet,
            "activity_count": row.activity_count,
            "volume_usd": float(row.volume_usd or 0),
            "last_seen": row.last_seen,
        })

    return {
        "lookback_minutes": lookback_minutes,
        "totals": {
            "events": len(recent_events),
            "total_volume_usd": total_notional,
            "buy_volume_usd": buy_notional,
            "sell_volume_usd": sell_notional,
        },
        "exposure": exposure,
        "assets": assets,
        "whale_wallets": whale_wallets,
    }


@app.get("/assets")
def assets(db: Session = Depends(get_db)):
    return db.query(Asset).all()
