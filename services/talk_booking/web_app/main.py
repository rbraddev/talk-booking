from fastapi import FastAPI, Depends
from sqlmodel import Session, SQLModel, create_engine, select

from models import TalkRequest, Address
from models.requests import AcceptTalkRequest, RejectTalkRequest, SubmitTalkRequest
from models.responses import TalkRequestDetails, TalkRequestList

from .config import load_config

app = FastAPI()
app_config = load_config()

engine = create_engine(app_config.SQLMODEL_DATABASE_URI, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/health-check/")
def health_check():
    return {"message": "OK"}


@app.post("/request-talk/", status_code=201, response_model=TalkRequestDetails)
def request_talk(submit_talk_request: SubmitTalkRequest, session: Session = Depends(get_session)):
    talk_request = TalkRequest(
        event_time=submit_talk_request.event_time,
        address=submit_talk_request.address,
        topic=submit_talk_request.topic,
        status="PENDING",
        duration_in_minutes=submit_talk_request.duration_in_minutes,
        requester=submit_talk_request.requester,
    )
    session.add(talk_request)
    session.commit()
    session.refresh(talk_request)
    return talk_request

@app.get("/talk-requests/", status_code=200, response_model=TalkRequestList)
def talk_requests(session: Session = Depends(get_session)):
    return {
        "results": [
            talk_request.dict() for talk_request in session.exec(select(TalkRequest)).all()
        ]
    }


@app.post("/talk-request/accept/", status_code=200, response_model=TalkRequestDetails)
def accept_talk_request(accept_talk_request_body: AcceptTalkRequest):
    return {
        "id": accept_talk_request_body.id,
        "event_time": "2021-10-03T10:30:00",
        "address": {
            "street": "Know Your Role Boulevard",
            "city": "Las Vegas",
            "state": "Nevada",
            "country": "USA",
        },
        "topic": "FastAPI with Pydantic",
        "status": "ACCEPTED",
        "duration_in_minutes": 45,
        "requester": "john@doe.com",
    }


@app.post("/talk-request/reject/", status_code=200, response_model=TalkRequestDetails)
def reject_talk_request(reject_talk_request_body: RejectTalkRequest):
    return {
        "id": reject_talk_request_body.id,
        "event_time": "2021-10-03T10:30:00",
        "address": {
            "street": "Know Your Role Boulevard",
            "city": "Las Vegas",
            "state": "Nevada",
            "country": "USA",
        },
        "topic": "FastAPI with Pydantic",
        "status": "REJECTED",
        "duration_in_minutes": 45,
        "requester": "john@doe.com",
    }
