# Log Analytics API

A small FastAPI service for collecting application logs and querying them with filtering, pagination, and simple analytics.

I built this because I wanted something closer to real backend work than the usual CRUD-style projects. Logs are something every system deals with sooner or later, so it felt like a more practical place to focus.

---

## Features

- create log records through an API  
- fetch a single log entry by id  
- list logs with filtering, pagination, and sorting  
- protect selected endpoints with JWT authentication  
- expose basic analytics (severity distribution, error trends, simple alert checks)  
- manage schema changes with Alembic  

---

## Tech stack

- Python  
- FastAPI  
- MySQL  
- SQLAlchemy  
- Alembic  
- Pytest  
- Docker / Docker Compose  

---

## Why I built it

While working on this, I noticed how quickly raw logs become hard to work with unless you add some structure on top. Even simple filtering and grouping already make a big difference.

I also wanted to move away from the typical “users/tasks” projects and build something a bit more operational. It’s still a small project, but the flow feels closer to something you’d actually run in a real service.

The alerting part came later. I kept it intentionally simple, but it helped make the project feel more complete.

---

## Project structure

```
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
---

## Main endpoints

The API is organized into a few main areas:

- `auth`  
- `health`  
- `logs`  
- `analytics`  

---

## Typical flow

1. authenticate  
2. send log events  
3. query logs by level, date, or source  
4. check analytics or alerts for patterns  

---

## Alerting

The API includes a simple alerting layer based on recent log activity.

Current checks include:

- spikes in `ERROR` / `CRITICAL` logs from the same source  
- repeated failed login events from the same IP address  

This part is intentionally lightweight so it stays easy to understand and doesn’t turn into a full monitoring system.

---

## Run locally

### With Docker

```bash
docker compose up --build
```

Once the containers are running, open:
- http://localhost:8000/docs
- http://localhost:8000/redoc

### Run tests

```bash
pytest
```

---

## Example log payload

```json
{
  "timestamp": "2026-03-20T10:30:00",
  "source": "auth-service",
  "host": "auth-node-1",
  "severity": "ERROR",
  "message": "Database connection timeout",
  "environment": "production",
  "event_type": "application_error",
  "status_code": 500,
  "ip_address": "192.168.1.20",
  "request_id": "req-12345"
}
```

---

## Example alert

```json
{
  "type": "error_spike",
  "severity": "high",
  "source": "auth-service",
  "count": 8,
  "window_minutes": 15,
  "message": "High number of ERROR logs detected for auth-service"
}
```

---

## Notes

This isn’t meant to replace a full logging or monitoring stack. The idea was to keep it small but still cover the kind of backend concerns you’d actually run into.

---

## Possible next improvements

- API key ingestion for service-to-service logging
- better handling of alert thresholds
- simple dashboard or UI on top of the API

