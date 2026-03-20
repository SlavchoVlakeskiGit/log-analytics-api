# Log Analytics API

A small FastAPI service for collecting application logs and querying them with filtering, pagination, and simple analytics.

I mainly built this because I wanted something a bit closer to real backend work than the usual CRUD examples.

## What it does

- create log records through an API
- fetch a single log entry by id
- list logs with filters, pagination, and sorting
- protect selected endpoints with JWT authentication
- expose summary endpoints for things like severity distribution, error trends, and repeated failed logins
- manage schema changes with Alembic

## Tech stack

- Python
- FastAPI
- MySQL
- SQLAlchemy
- Alembic
- Pytest
- Docker / Docker Compose

## Why I built it

One thing I realized while building this is that even simple log data becomes useful once you add a bit of filtering and aggregation on top.

A lot of beginner backend projects stop at users, products, or tasks. I wanted something that still stays small enough for a portfolio, but uses a workflow that feels more operational.

The analytics part was probably the most useful addition because it pushed the project beyond basic create/read endpoints and made the data model feel more purposeful.

## Project structure

```text
log-analytics-api/
├── alembic/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   └── services/
├── assets/
├── scripts/
├── tests/
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── requirements.txt
```

## Main endpoints

Examples of the main areas covered by the API:

- auth
- health
- logs
- analytics

## Typical flow

1. authenticate
2. send log events
3. query logs by level, date, or source
4. review summary endpoints for patterns in the data

## Run locally

```bash
git clone https://github.com/SlavchoVlakeskiGit/log-analytics-api.git
cd log-analytics-api
docker-compose up --build
alembic upgrade head
```

Open `/docs` in the browser to test the API.

## Example log payload

```json
{
  "timestamp": "2026-03-20T10:14:00Z",
  "level": "ERROR",
  "service": "auth-service",
  "message": "Invalid token",
  "source_ip": "10.0.0.24"
}
```

## Testing

```bash
pytest
```

## Notes

This is not meant to be a full monitoring platform. I kept the scope fairly tight so the main backend pieces stay clear and easy to follow.

## Possible next improvements

- simple alert rules
- demo seed script for sample logs
- API key ingestion for service-to-service logging
- more analytics around repeated failures or spikes
