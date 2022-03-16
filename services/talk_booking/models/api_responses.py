import datetime

from pydantic import EmailStr, PositiveInt
from sqlmodel import SQLModel

from models import Address
from models.talk_request import TalkRequestStatus


class TalkRequestDetails(SQLModel):
    id: str
    event_time: datetime.datetime
    address: Address
    topic: str
    duration_in_minutes: PositiveInt
    requester: EmailStr
    status: TalkRequestStatus
