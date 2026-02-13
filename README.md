# Venora API

Lightweight FastAPI backend for Venora — auth + users + basic routes used by the Venora UI.

## Quick overview
- Framework: FastAPI
- ASGI server: Uvicorn
- DB: set via `DATABASE_URL` (examples below)
- Project entry: `app/main.py`

## Prerequisites
- Python 3.10+ (recommended)
- `pip` / virtualenv

## Install
1. Create and activate a virtual environment

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1   # PowerShell
# or
.\.venv\Scripts\activate.bat  # cmd
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration
Set environment variables used by the app before running. Minimal recommended variables:

- `DATABASE_URL` — SQLAlchemy database URL. Examples:
  - SQLite (dev): `sqlite:///./venora.db`
  - MySQL: `mysql+pymysql://user:pass@localhost:3306/venora_db`
- `SECRET_KEY` — secret for signing JWTs
- `ACCESS_TOKEN_EXPIRE_MINUTES` — token lifetime (integer minutes)
- `ALGORITHM` — JWT algorithm (e.g. `HS256`)

You can export these in your shell or create a `.env` loader if you prefer.

## Database
- The project contains `app/create_tables.py` and `app/reset_users_table.py` helpers.
- To create tables quickly (development):

```bash
python app/create_tables.py
# or reset the users table
python app/reset_users_table.py
```

- If you use Alembic for migrations, run your migrations with Alembic (project already contains `alembic/` skeleton).

## Seed data
- A small seeder exists: `app/seed_users.py`. Run it to create initial accounts (SuperAdmin/SubAdmin/Customer) in development.

```bash
python app/seed_users.py
```

## Run (development)

Start the API with Uvicorn (Makefile helper also available):

```bash
# from repository root
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Or using Makefile (if available):
make start-dev
```

The API will be available at `http://localhost:8000`.

## Important endpoints
- `GET /api/health` — health check (may differ; check `app/routers/health.py`)
- `POST /auth/register` — register a new user (body depends on schema in `app/schemas/user.py`)
- `POST /auth/login` — login returns JWT access token

Check `app/routers` for all available routes and exact request/response formats.

## Testing
- If tests are added, run with `pytest`.

## Docker
- You can containerize with the provided `Dockerfile` and `docker-compose.yml` (if present).

## Common commands
- Install dependencies: `pip install -r requirements.txt`
- Start dev server: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Create DB tables: `python app/create_tables.py`
- Seed users: `python app/seed_users.py`

## Notes
- Keep secrets out of source control. Use environment variables or a secrets manager in production.
- Adjust `DATABASE_URL` and JWT settings for your environment.

If you want, I can add example `.env` and a Postman collection quick-start for the seeded accounts.