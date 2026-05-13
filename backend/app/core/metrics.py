from prometheus_client import Counter, Gauge, Histogram

request_duration_seconds = Histogram(
    "request_duration_seconds",
    "Request duration histogram",
    ["method", "path", "status"],
)

events_ingested_total = Counter(
    "events_ingested_total",
    "Total number of ingested events",
)

cache_hit_rate = Gauge(
    "cache_hit_rate",
    "Cache hit rate",
)

kafka_consumer_lag = Gauge(
    "kafka_consumer_lag",
    "Kafka consumer lag",
)

cache_hits_total = Counter("cache_hits_total", "Cache hit count")
cache_misses_total = Counter("cache_misses_total", "Cache miss count")
