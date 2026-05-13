# AI Analytics API Platform

## Phase 1: Local Dev Environment
- PostgreSQL 16, Redis 7, Zookeeper/Kafka, Kafdrop via `docker-compose.yml`
- `.env.example` for all required runtime settings
- `Makefile` commands: `make dev`, `make test`, `make migrate`, `make build`

## Phase 2: FastAPI Backend Foundation
- FastAPI app factory + lifespan
- SQLAlchemy 2.0 models (`users`, `api_keys`, `events` with JSONB properties)
- Alembic configuration and initial migration
- Pydantic v2 schemas for request/response contracts
- Structured JSON logging and Lambda-optimized connection pooling

## Phase 3: Core API Endpoints
- Event ingestion, analytics summary/timeseries/funnels, auth register/login/refresh
- Health + Prometheus metrics endpoints
- RFC 7807 problem-details exception handlers
- JWT + bcrypt helpers
- Unit/integration tests for core contracts

## Phase 4: Redis Caching and Rate Limiting
- Redis-backed analytics cache with TTL and startup warming
- Sliding-window rate limiting using Redis sorted sets (1000 req/min default)
- In-memory fallback for local/offline test runs
- Cache hit/miss counters and cache hit-rate gauge

## Phase 5: Kafka Event Pipeline
- Kafka producer for event ingestion path
- Background Kafka consumer worker with consumer-group configuration
- Batch inserts into PostgreSQL via SQLAlchemy sessions
- Dead-letter topic publishing after retry exhaustion
- Consumer lag metric (`kafka_consumer_lag`) updates during polling

## Phase 6: React TypeScript Dashboard
- React 18 + TypeScript dashboard scaffolded with Vite
- Login/Register flow with token storage + refresh handling hook
- Dashboard cards for events, users, p95 latency, and error rate
- Time range selector with 30s auto-refresh data hook
- Recharts visualizations for timeseries and funnels
- Top pages sortable/paginated table
- API key create/list/revoke panel
- Typed Axios API client and TailwindCSS styling
- UI screenshot: `frontend/dashboard-phase6.png`

## Quick start
```bash
cp .env.example .env
make dev
```
