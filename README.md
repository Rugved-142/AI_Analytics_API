# AI Analytics API Platform

## Phase 1: Local Dev Environment

### Local services
- PostgreSQL 16
- Redis 7
- Zookeeper + Kafka
- Kafdrop UI

### Setup
1. Copy env file: `cp .env.example .env`
2. Start stack: `make dev`

### Common commands
- `make test`
- `make migrate`
- `make build`

## Phase 2: FastAPI Backend Foundation

### Backend stack
- FastAPI app factory with lifespan startup/shutdown
- SQLAlchemy 2.0 models: `users`, `api_keys`, `events`
- Alembic migration for all base tables
- Pydantic v2 request/response schemas
- JSON structured logging
- Lambda-oriented DB pooling (`pool_pre_ping`, bounded pool size, recycle)

### Backend layout
- `backend/app/main.py`
- `backend/app/core/*`
- `backend/app/db/*`
- `backend/alembic/*`
