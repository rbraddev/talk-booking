import datetime
import uuid

from sqlmodel import Session, select

from models import Address, TalkRequest


def test_talk_request(session: Session):
    """
    GIVEN talk request and database
    WHEN talk request is saved
    THEN in can accessed by its id or listed
    """
    talk_request = TalkRequest(
        id=str(uuid.uuid4()),
        event_time=datetime.datetime.utcnow(),
        address=Address(
            street="Sunny street 42",
            city="Awesome city",
            state="Best state",
            country="Ireland",
        ),
        duration_in_minutes=45,
        topic="Python type checking",
        requester="john@doe.com",
        status="PENDING",
    )

    session.add(talk_request)
    session.commit()


    assert session.exec(select(TalkRequest))[0] == talk_request
    assert session.exec(select(TalkRequest).where(TalkRequest.id == talk_request.id)) == talk_request
