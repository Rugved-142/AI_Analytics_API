from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analytics, auth, events, health
from app.core.config import get_settings
from app.core.logging import configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
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
    app.include_router(events.router, prefix=settings.api_v1_prefix)
    app.include_router(analytics.router, prefix=settings.api_v1_prefix)
    app.include_router(auth.router)
    app.include_router(health.router)
    return app


app = create_app()
