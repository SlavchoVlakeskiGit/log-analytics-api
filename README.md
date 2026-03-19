# Log Analytics API

A FastAPI backend for storing, filtering, and analyzing application logs with MySQL.

I built this project to practice API design, database modeling, authentication, pagination, and analytics endpoints in one backend application.

## What it does

- create log records through an API
- fetch a single log entry by id
- list logs with filters, pagination, and sorting
- protect selected endpoints with JWT authentication
- expose a few summary endpoints for things like severity distribution, error trends, and repeated failed logins
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

A lot of beginner backend projects stop at users, products, or tasks.

I wanted to build something that still stays small enough for a portfolio, but uses a data model and endpoint set that feels more like backend work than a tutorial exercise.

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

The README should stay honest here: the project is not a full monitoring platform. It is a focused practice project that shows the backend building blocks clearly.

## Running locally

### 1. Clone the repo

```bash
git clone https://github.com/SlavchoVlakeskiGit/log-analytics-api.git
cd log-analytics-api
```

### 2. Create and configure environment variables

Copy `.env.example` and fill in your local values.

### 3. Start the app and database

```bash
docker-compose up --build
```

### 4. Run migrations

```bash
alembic upgrade head
```

### 5. Open the docs

Open `/docs` in the browser to test the API.

## Testing

```bash
pytest
```

## Notes

A few things I would improve next if I kept extending this project:

- better seed data and test fixtures
- more complete validation around log sources and event types
- clearer separation between analytics queries and business rules
- stronger error handling around malformed ingestion payloads

## Screenshots

Add 1-2 screenshots only if they help show the API docs or example responses. For this kind of project, request/response examples are usually more useful than too many images.
