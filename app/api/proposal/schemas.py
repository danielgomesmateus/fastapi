from pydantic import BaseModel

from app.api.client.schemas import Client
from app.api.property.schemas import Property


class ProposalCreate(BaseModel):
    client_id: int
    property_id: int
    name: str
    amount: float


class Proposal(BaseModel):
    id: int
    client: Client
    property: Property
    name: str
    amount: float

    class Config:
        orm_mode = True