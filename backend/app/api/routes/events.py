from fastapi import APIRouter, status

from app.api.schemas import EventIngestRequest, EventResponse

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EventResponse, status_code=status.HTTP_202_ACCEPTED)
def ingest_event(payload: EventIngestRequest) -> EventResponse:
    return EventResponse(id=0, message=f"accepted:{payload.event_type}")
