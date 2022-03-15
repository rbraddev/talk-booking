import datetime
from enum import Enum

from pydantic import EmailStr, PositiveInt
from sqlmodel import SQLModel

from .address import Address


class TalkRequestStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class TalkRequest(SQLModel):
    id: str
    event_time: datetime.datetime
    address: Address
    topic: str
    duration_in_minutes: PositiveInt
    requester: EmailStr
    status: TalkRequestStatus

    @property
    def is_rejected(self):
        return self.status == TalkRequestStatus.REJECTED
