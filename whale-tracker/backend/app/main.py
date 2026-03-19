from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db.session import Base, engine, get_db
from app.models.entities import Alert, Rule, Asset
from app.schemas.api import RuleIn, RuleOut, AlertOut, SignalOut, WhaleOrderOut, AssistantBriefOut
from app.signals.service import generate_crypto_signals, get_whale_orders, get_assistant_brief
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


@app.get("/assets")
def assets(db: Session = Depends(get_db)):
    return db.query(Asset).all()


@app.get("/signals", response_model=list[SignalOut])
def signals(db: Session = Depends(get_db)):
    return generate_crypto_signals(db)


@app.get("/whale-orders", response_model=list[WhaleOrderOut])
def whale_orders(symbol: str | None = None, limit: int = 30, db: Session = Depends(get_db)):
    return get_whale_orders(db, symbol=symbol, limit=min(limit, 100))


@app.get("/assistant", response_model=AssistantBriefOut)
async def assistant(db: Session = Depends(get_db)):
    return await get_assistant_brief(db)
