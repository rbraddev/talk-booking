from pydantic import BaseModel, Field

from models import Address, TalkRequest


class TalkRequestDetails(TalkRequest):
    response_address: Address = Field(alias="address")


class TalkRequestList(BaseModel):
    results: list[TalkRequestDetails]
