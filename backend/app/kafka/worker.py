from app.kafka.consumer import EventConsumer


def run_worker() -> None:
    consumer = EventConsumer()
    consumer.consume_forever()


if __name__ == "__main__":
    run_worker()
