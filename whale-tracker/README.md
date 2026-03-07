# WhaleScope

Production-style full-stack whale activity dashboard for Crypto + XAUUSD + XAGUSD.

## Project tree

```text
whale-tracker/
├── backend/
│   ├── app/
│   │   ├── alerts/engine.py
│   │   ├── api/routes.py
│   │   ├── core/{config.py,security.py}
│   │   ├── db/session.py
│   │   ├── models/entities.py
│   │   ├── providers/{base.py,factory.py,mock_provider.py}
│   │   ├── schemas/api.py
│   │   ├── services/{state.py,streamer.py,ws.py}
│   │   ├── signals/detectors.py
│   │   ├── utils/normalizer.py
│   │   ├── workers/celery_app.py
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   ├── seed_demo.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/ (dashboard + asset detail + alerts + signals + watchlist + settings)
│   ├── components/
│   ├── lib/api.ts
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Features
- Live multi-asset dashboard (Crypto / XAUUSD / XAGUSD)
- Realtime event stream over WebSocket with polling-capable HTTP endpoints
- Alert + signal engine with confidence scoring and severity model
- Provider abstraction (`BaseMarketDataProvider`) and demo mock provider
- Signal source labels: `confirmed trade flow`, `exchange liquidation/open interest data`, `volume spike proxy`, `futures tape proxy`, `mock/demo data`
- Data source confidence labels in UI (`high/medium/low confidence`)
- Watchlist API + settings controls (thresholds, confidence cutoff, per-asset tracking)
- CSV alerts export endpoint
- JWT admin auth endpoint
- Demo/live and provider health status badges
- Celery worker scaffold + Redis + PostgreSQL

## Run locally

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

App URLs:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs

## Run with Docker
```bash
cp .env.example .env
docker compose up --build
```

## Demo mode behavior
If no live credentials are configured, WhaleScope runs in `DEMO_MODE=true` and:
- streams realistic synthetic trade/ticker events
- simulates whale trades and derived pressure
- clearly labels source as `mock/demo data`

## Provider architecture
- `BaseMarketDataProvider` standardizes:
  - `subscribe_trades()`
  - `subscribe_ticker()`
  - `fetch_ohlcv()`
  - `fetch_open_interest()`
  - `fetch_liquidations()`
  - `health_check()`
- Add real adapters (Binance/Bybit/broker feeds) by implementing the same interface.

## Security + config
- `.env` driven settings (no hardcoded runtime secrets)
- JWT login endpoint `/api/auth/login`
- CORS configured via `CORS_ORIGINS`

## Tests
```bash
cd backend
pytest -q
```

## Notes on realism
XAUUSD/XAGUSD direct institutional tape is not fabricated. When direct flow is unavailable, WhaleScope uses derived proxies and labels source + confidence explicitly.

