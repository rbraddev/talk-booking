import datetime

from pydantic import BaseModel, EmailStr, PositiveInt

from .address import Address


class SubmitTalkRequest(BaseModel):
    event_time: datetime.datetime
    address: Address
    topic: str
    duration_in_minutes: PositiveInt
    requester: EmailStr


class AcceptTalkRequest(BaseModel):
    id: str


class RejectTalkRequest(BaseModel):
    id: str
