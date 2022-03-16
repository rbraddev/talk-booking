import datetime

from pydantic import PositiveInt, EmailStr
from sqlmodel import SQLModel

from .address import Address


class SubmitTalkRequest(SQLModel):
    event_time: datetime.datetime
    address: Address
    topic: str
    duration_in_minutes: PositiveInt
    requester: EmailStr
