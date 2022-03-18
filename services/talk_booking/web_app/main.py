import pathlib
import uuid

from fastapi import FastAPI
from sqlmodel import Session, SQLModel, create_engine

from models.api_requests import AcceptTalkRequest, RejectTalkRequest, SubmitTalkRequest
from models.api_responses import TalkRequestDetails, TalkRequestList

from .config import load_config

app = FastAPI()
app_config = load_config()

connect_args = {"check_same_thread": False}
engine = create_engine(app_config.SQLMODEL_DATABASE_URI, echo=False, connect_args=connect_args)


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
def request_talk(submit_talk_request: SubmitTalkRequest):
    return {
        "id": "unique_id",
        "event_time": submit_talk_request.event_time,
        "address": submit_talk_request.address,
        "topic": submit_talk_request.topic,
        "status": "PENDING",
        "duration_in_minutes": submit_talk_request.duration_in_minutes,
        "requester": submit_talk_request.requester,
    }


@app.get("/talk-requests/", status_code=200, response_model=TalkRequestList)
def talk_requests():
    return {
        "results": [
            {
                "id": "unique_id",
                "event_time": "2021-10-03T10:30:00",
                "address": {
                    "street": "Know Your Role Boulevard",
                    "city": "Las Vegas",
                    "state": "Nevada",
                    "country": "USA",
                },
                "topic": "FastAPI with Pydantic",
                "status": "PENDING",
                "duration_in_minutes": 45,
                "requester": "john@doe.com",
            }
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
