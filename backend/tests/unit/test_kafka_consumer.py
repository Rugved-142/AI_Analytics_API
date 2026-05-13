from app.kafka.consumer import EventConsumer


class DummySession:
    def __init__(self) -> None:
        self.items = []

    def add_all(self, records) -> None:
        self.items.extend(records)

    def commit(self) -> None:
        return None


def test_batch_insert_adds_records() -> None:
    consumer = EventConsumer.__new__(EventConsumer)
    session = DummySession()
    consumer._batch_insert(
        session,
        [{"user_id": 1, "session_id": "abc", "event_type": "page_view", "properties": {"page": "/"}}],
    )
    assert len(session.items) == 1
    assert session.items[0].event_type == "page_view"
