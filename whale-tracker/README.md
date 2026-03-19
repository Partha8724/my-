# Whale Tracker & Cross-Asset Alert (MVP)

Production-minded MVP for monitoring crypto whale flows, unusual stock activity, and XAUUSD movement.

## Current Status
- Backend tests are passing.
- Frontend production build is passing.
- Windows helper scripts are included:
  - `start.bat` starts backend and frontend in separate CMD windows.
  - `stop.bat` closes those windows.
- Default demo mode works with mock providers, so you can run the app without paid APIs.

## Windows Quick Start
1. Open `C:\Users\HP\crypto-whale-tracker\whale-tracker`
2. Double-click `start.bat`
3. If prompted, allow it to open `http://localhost:5173`
4. To stop both services later, double-click `stop.bat`

## GitHub Publish Checklist
1. Keep `.env` private and only commit `.env.example`
2. Do not commit local files like `frontend/node_modules`, `backend/whale_tracker.db`, or pytest temp folders
3. Keep `frontend/package-lock.json` committed so installs stay reproducible
4. Run `pytest -q` in `backend`
5. Run `npm run build` in `frontend`
6. Commit from the repository root after reviewing `git status`

## Stack
- Backend: FastAPI + APScheduler + SQLAlchemy (SQLite default)
- Frontend: React (Vite)
- Notifications: Telegram + SMTP email
- Infra: Docker Compose (includes Redis service for future Celery upgrade)

## Features
- Unified asset registry (`asset_id`, `asset_type`, `symbol`, `venue`)
- Unified event normalization for crypto/stocks/metals
- Rule engine with:
  - `threshold_usd`
  - `percent_move`
  - `volume_multiple`
  - `volatility_threshold`
  - `key_levels`
  - `cooldown_minutes`
  - `quiet_hours`
- Dedupe key per rule/asset/event time bucket
- Alert persistence and API feed
- Dashboard pages in one UI:
  - Alerts feed
  - Rules/config
  - Asset watchlist
  - Health status
- `/health` endpoint and provider error capture
- Unit tests for trigger + dedupe behavior

## Data Providers
### Crypto
- `mock` provider (default; no key required)
- Whale Alert official API (`CRYPTO_PROVIDER=whale` + `WHALE_ALERT_API_KEY`)
- Binance trade spike signal via CCXT public endpoint (enabled by default)

### Stocks
- `mock` provider included for free running demo
- Abstraction point is in `app/providers/` for plugging Alpaca / IEX / Polygon providers.

### XAUUSD
- `mock` provider (default)
- Twelve Data (`XAU_PROVIDER=twelve` + `TWELVEDATA_API_KEY`)

## Setup
1. Copy env file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and add keys you own.
3. Run backend locally:
   ```bash
   cd backend
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   python -m app.cli
   uvicorn app.main:app --reload
   ```
4. Run frontend locally:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Docker Compose
```bash
docker compose up --build
```
- API: http://localhost:8000
- Frontend: http://localhost:5173

## Seed demo assets/rules
```bash
cd backend
python -m app.cli
```

## Telegram Configuration
1. Create a bot with BotFather and get token.
2. Get your target chat ID.
3. Set:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

## Email Configuration
Set SMTP values:
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `EMAIL_FROM`, `EMAIL_TO`

## Testing
```bash
cd backend
pytest -q
```

## MVP to Production Upgrades
- Replace APScheduler with Celery workers + Redis queues.
- Add PostgreSQL and Alembic migrations.
- Add auth (JWT or magic link) and multi-user rule ownership.
- Add Discord notifier and webhook-based incident routing.
- Add historical analytics and charts for signal quality.

## Extending to more chains/assets
1. Implement a new provider class in `app/providers/` returning `NormalizedEvent` objects.
2. Register it in `IngestionService.get_providers()`.
3. Add new symbols to `Asset` watchlist via UI or seed CLI.
4. Expand event payload fields as needed (e.g., gas, chain_id, venue depth).
5. Add specialized rules per asset type while keeping normalized schema stable.
