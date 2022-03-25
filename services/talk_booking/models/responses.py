from pydantic import BaseModel, Field

from models import Address, TalkRequestBase


class TalkRequestDetails(TalkRequestBase):
    id: int
    response_address: Address = Field(alias="address")


class TalkRequestList(BaseModel):
    results: list[TalkRequestDetails]
