import datetime

from pydantic import EmailStr, PositiveInt
from sqlmodel import SQLModel

from .address import Address


class SubmitTalkRequest(SQLModel):
    event_time: datetime.datetime
    address: Address
    topic: str
    duration_in_minutes: PositiveInt
    requester: EmailStr
