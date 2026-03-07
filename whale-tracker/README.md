# WhaleScope

Production-style full-stack whale activity dashboard for **Crypto, XAUUSD, XAGUSD** with realtime signals, advanced proxy analytics, provider abstraction, and demo mode.

## What improved
- Noise reduction pipeline:
  - per-symbol cooldown
  - duplicate alert suppression
  - confidence threshold filter
  - multi-hit confirmation window
- Advanced analytics:
  - rolling buy/sell imbalance
  - cumulative delta proxy
  - volatility filter
  - trend regime filter
- Professional dashboard UI:
  - stronger dark theme
  - heatmap
  - top movers panel
  - signal breakdown modal
- Deployment polish:
  - healthchecks in compose
  - structured config validation + prod guardrails
  - logging setup
  - ingestion retry logic
- More realistic demo simulator:
  - whale bursts
  - periodic volume spikes
  - regime switches for XAUUSD/XAGUSD

## Project tree

```text
whale-tracker/
  backend/
    app/
      api/ core/ models/ schemas/ services/ providers/ alerts/ signals/ db/ workers/ utils/
    alembic/
    tests/
    Dockerfile
  frontend/
    app/ components/ lib/ types/
    Dockerfile
  docker-compose.yml
  .env.example
```

## Setup

### Local
```bash
cd backend
pytest -q
uvicorn app.main:app --reload --port 8000
```

```bash
cd frontend
npm install
npm run dev
```

### Docker
```bash
cp .env.example .env
docker compose up --build
```

## API
- `GET /health`
- `POST /api/auth/login`
- `GET /api/assets`
- `GET /api/settings`
- `PUT /api/settings`
- `GET /api/watchlist`
- `POST /api/watchlist`
- `DELETE /api/watchlist/{id}`
- `GET /api/alerts`
- `GET /api/alerts/export.csv`
- `GET /api/signals`
- `GET /api/providers/status`
- `GET /api/market/overview`
- `GET /api/market/{symbol}`
- `GET /api/market/{symbol}/history`
- `WS /ws/stream`

## Realism policy
For XAUUSD/XAGUSD, when direct institutional flow is unavailable, WhaleScope emits labeled derived/proxy signals and confidence context.
