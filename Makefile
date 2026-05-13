SHELL := /bin/bash

.PHONY: dev test migrate build

dev:
docker compose up -d --build

test:
cd backend && pytest -q

migrate:
cd backend && alembic upgrade head

build:
cd backend && docker build -t ai-analytics-backend .
cd frontend && npm run build
