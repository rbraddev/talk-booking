from fastapi import FastAPI

from models import SubmitTalkRequest, TalkRequestDetails

app = FastAPI()


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
