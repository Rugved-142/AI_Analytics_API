from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.schemas import EventIngestRequest, EventResponse
from app.core.metrics import events_ingested_total
from app.db.models.event import Event
from app.db.session import get_db
from app.kafka.producer import EventProducer

router = APIRouter(prefix="/events", tags=["events"])
producer = EventProducer()


@router.post("", response_model=EventResponse, status_code=status.HTTP_202_ACCEPTED)
def ingest_event(payload: EventIngestRequest, db: Session = Depends(get_db)) -> EventResponse:
    event = Event(
        user_id=payload.user_id,
        session_id=payload.session_id,
        event_type=payload.event_type,
        properties=payload.properties,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    producer.publish_event(
        {
            "id": event.id,
            "user_id": event.user_id,
            "session_id": event.session_id,
            "event_type": event.event_type,
            "properties": event.properties,
        }
    )
    events_ingested_total.inc()
    return EventResponse(id=event.id, message="accepted")
