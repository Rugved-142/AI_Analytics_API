import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analytics, auth, events, health
from app.core.config import get_settings
from app.core.errors import register_problem_handlers
from app.core.logging import configure_logging
from app.core.metrics import request_duration_seconds
from app.services.cache import warm_cache


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    warm_cache()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="AI Analytics API", version="1.0.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def add_observability(request: Request, call_next) -> Response:
        correlation_id = request.headers.get("x-correlation-id", str(uuid.uuid4()))
        start = time.perf_counter()
        response = await call_next(request)
        latency = time.perf_counter() - start
        request_duration_seconds.labels(request.method, request.url.path, str(response.status_code)).observe(latency)
        response.headers["x-correlation-id"] = correlation_id
        return response

    register_problem_handlers(app)
    app.include_router(events.router, prefix=settings.api_v1_prefix)
    app.include_router(analytics.router, prefix=settings.api_v1_prefix)
    app.include_router(auth.router)
    app.include_router(health.router)
    return app


app = create_app()
