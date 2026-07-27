# Smart Job Market Radar & Application Tracker

Self-hosted system that monitors job board APIs, scores postings against your
profile using semantic matching, and tracks your application pipeline.

## Status
🚧 Phase 0 — project scaffold

## Local setup
1. Copy `.env.example` to `.env` and fill in the values (see below).
2. Start Postgres + Redis: `docker-compose up -d`
3. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Run the API: `uvicorn backend.app.main:app --reload`
5. Confirm it's alive: visit http://localhost:8000/health — should return `{"status": "ok"}`

## Getting API keys
- **Adzuna**: register at https://developer.adzuna.com/ — gives you an `app_id` and `app_key` immediately.
- **Greenhouse / Lever**: no key needed — public per-company job board endpoints.
- **RemoteOK**: no key needed — public JSON feed.

## Architecture
See project roadmap doc for full details on services, phases, and skill mapping.
