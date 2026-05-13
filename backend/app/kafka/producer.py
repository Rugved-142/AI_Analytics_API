import json
import logging
from typing import Any

from kafka import KafkaProducer
from kafka.errors import KafkaError

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class EventProducer:
    def __init__(self) -> None:
        try:
            self._producer: KafkaProducer | None = KafkaProducer(
                bootstrap_servers=settings.kafka_bootstrap_servers,
                value_serializer=lambda value: json.dumps(value).encode("utf-8"),
                retries=3,
            )
        except KafkaError:
            logger.exception("Kafka initialization failed")
            self._producer = None

    def publish_event(self, payload: dict[str, Any]) -> None:
        if self._producer is None:
            return
        future = self._producer.send(settings.kafka_events_topic, payload)
        try:
            future.get(timeout=3)
        except KafkaError as exc:
            logger.exception("Kafka publish failed", extra={"error": str(exc)})
