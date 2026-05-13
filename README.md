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

## Quick start
```bash
cp .env.example .env
make dev
```
