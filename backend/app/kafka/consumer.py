import json
import logging
import time
from typing import Any

from kafka import KafkaConsumer
from kafka.errors import KafkaError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.metrics import kafka_consumer_lag
from app.db.models.event import Event
from app.db.session import SessionLocal
from app.kafka.dlq import DeadLetterProducer

logger = logging.getLogger(__name__)
settings = get_settings()


class EventConsumer:
    def __init__(self) -> None:
        self.consumer = KafkaConsumer(
            settings.kafka_events_topic,
            bootstrap_servers=settings.kafka_bootstrap_servers,
            group_id=settings.kafka_consumer_group,
            value_deserializer=lambda value: json.loads(value.decode("utf-8")),
            enable_auto_commit=False,
            auto_offset_reset="earliest",
        )
        self.dlq = DeadLetterProducer()

    def _batch_insert(self, db: Session, batch: list[dict[str, Any]]) -> None:
        records = [
            Event(
                user_id=item.get("user_id"),
                session_id=str(item.get("session_id", "")),
                event_type=str(item.get("event_type", "unknown")),
                properties=item.get("properties", {}),
            )
            for item in batch
        ]
        db.add_all(records)
        db.commit()

    def consume_forever(self, batch_size: int = 100, poll_timeout_ms: int = 1000, max_retries: int = 3) -> None:
        retry_counts: dict[str, int] = {}
        batch: list[dict[str, Any]] = []

        while True:
            try:
                messages = self.consumer.poll(timeout_ms=poll_timeout_ms, max_records=batch_size)
            except KafkaError:
                logger.exception("Kafka poll failed")
                time.sleep(1)
                continue

            total_messages = sum(len(records) for records in messages.values())
            kafka_consumer_lag.set(float(total_messages))

            for _, records in messages.items():
                for record in records:
                    payload = record.value
                    key = f"{record.topic}:{record.partition}:{record.offset}"
                    try:
                        batch.append(payload)
                    except Exception:
                        retries = retry_counts.get(key, 0) + 1
                        retry_counts[key] = retries
                        if retries >= max_retries:
                            self.dlq.publish(payload)

            if batch:
                with SessionLocal() as db:
                    self._batch_insert(db, batch)
                batch.clear()
                self.consumer.commit()
