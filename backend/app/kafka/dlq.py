import json
from typing import Any

from kafka import KafkaProducer

from app.core.config import get_settings

settings = get_settings()


class DeadLetterProducer:
    def __init__(self) -> None:
        self._producer = KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
            retries=3,
        )

    def publish(self, payload: dict[str, Any]) -> None:
        self._producer.send(settings.kafka_dlq_topic, payload)
        self._producer.flush(timeout=3)
