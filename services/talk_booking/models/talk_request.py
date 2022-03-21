import datetime
from enum import Enum
from typing import Optional

from pydantic import EmailStr, PositiveInt
from sqlmodel import SQLModel, Field, JSON, Column

from .address import Address


class TalkRequestStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class TalkRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_time: datetime.datetime
    address: dict = Field(sa_column=Column(JSON))
    topic: str
    duration_in_minutes: PositiveInt
    requester: EmailStr
    status: TalkRequestStatus

    @property
    def is_rejected(self):
        return self.status == TalkRequestStatus.REJECTED
