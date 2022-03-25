import datetime
from enum import Enum
from typing import Optional

from pydantic import EmailStr, PositiveInt
from sqlmodel import JSON, Column, Field, SQLModel


class TalkRequestStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class TalkRequestBase(SQLModel):
    event_time: datetime.datetime
    address: dict = Field(sa_column=Column(JSON))
    topic: str
    duration_in_minutes: PositiveInt
    requester: EmailStr
    status: TalkRequestStatus


class TalkRequest(TalkRequestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    @property
    def is_rejected(self):
        return self.status == TalkRequestStatus.REJECTED

    def accept(self):
        self.status = TalkRequestStatus.ACCEPTED

    def reject(self):
        self.status = TalkRequestStatus.REJECTED
