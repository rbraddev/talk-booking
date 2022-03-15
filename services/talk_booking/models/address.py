from sqlmodel import SQLModel


class Address(SQLModel):
    street: str
    city: str
    state: str
    country: str
