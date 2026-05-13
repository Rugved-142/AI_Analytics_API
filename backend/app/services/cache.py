import json
from collections.abc import Callable
from typing import Any, TypeVar

import redis

from app.core.config import get_settings
from app.core.metrics import cache_hit_rate, cache_hits_total, cache_misses_total

settings = get_settings()


class InMemoryCache:
    def __init__(self) -> None:
        self.store: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        return self.store.get(key)

    def setex(self, key: str, _ttl: int, value: str) -> None:
        self.store[key] = value


cache_backend: redis.Redis | InMemoryCache
try:
    cache_backend = redis.Redis.from_url(settings.redis_url, decode_responses=True)
    cache_backend.ping()
except redis.RedisError:
    cache_backend = InMemoryCache()

T = TypeVar("T")


def _update_rate() -> None:
    hits = float(cache_hits_total._value.get())
    misses = float(cache_misses_total._value.get())
    total = hits + misses
    cache_hit_rate.set((hits / total) if total else 0.0)


def get_or_set_json(key: str, ttl: int, factory: Callable[[], T]) -> T:
    cached = cache_backend.get(key)
    if cached is not None:
        cache_hits_total.inc()
        _update_rate()
        return json.loads(cached)

    cache_misses_total.inc()
    _update_rate()
    value = factory()
    cache_backend.setex(key, ttl, json.dumps(value, default=str))
    return value


def warm_cache() -> None:
    defaults: dict[str, Any] = {
        "analytics:summary:1:10": {"total_events": 0, "unique_users": 0, "top_pages": [], "pagination": {"page": 1, "page_size": 10, "total": 0}},
        "analytics:timeseries:1h:1:100": {"granularity": "1h", "data": [], "pagination": {"page": 1, "page_size": 100, "total": 0}},
    }
    for key, value in defaults.items():
        cache_backend.setex(key, settings.redis_cache_ttl_seconds, json.dumps(value))
