import time

import redis

from app.core.config import get_settings
from app.core.errors import ProblemException
from app.services.cache import InMemoryCache, cache_backend

settings = get_settings()


def enforce_rate_limit(api_key: str) -> None:
    if not api_key:
        return

    now = time.time()
    window_start = now - 60
    key = f"ratelimit:{api_key}"

    if isinstance(cache_backend, InMemoryCache):
        history_raw = cache_backend.get(key)
        history = [float(item) for item in history_raw.split(",")] if history_raw else []
        history = [item for item in history if item >= window_start]
        if len(history) >= settings.rate_limit_per_minute:
            raise ProblemException(status_code=429, title="Too Many Requests", detail="Rate limit exceeded")
        history.append(now)
        cache_backend.setex(key, 60, ",".join(str(item) for item in history))
        return

    assert isinstance(cache_backend, redis.Redis)
    pipeline = cache_backend.pipeline()
    pipeline.zremrangebyscore(key, 0, window_start)
    pipeline.zcard(key)
    pipeline.zadd(key, {str(now): now})
    pipeline.expire(key, 60)
    _, count, _, _ = pipeline.execute()

    if int(count) >= settings.rate_limit_per_minute:
        raise ProblemException(status_code=429, title="Too Many Requests", detail="Rate limit exceeded")
