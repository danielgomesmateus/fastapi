from pydantic import BaseModel


class ClientCreate(BaseModel):
    name: str
    last_name: str
    email: str


class Client(BaseModel):
    id: int
    name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True