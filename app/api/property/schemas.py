from pydantic import BaseModel
from typing import List


class PropertyCreate(BaseModel):
    name: str
    address: str
    description: str
    characteristics: str
    property_type: str
    goal: str
    real_estate_id: int


class Property(BaseModel):
    id: int
    name: str
    address: str
    description: str
    characteristics: str
    property_type: str
    goal: str

    class Config:
        orm_mode = True


class RealEstateCreate(BaseModel):
    name: str
    address: str


class RealEstate(BaseModel):
    id: int
    name: str
    address: str
    properties: List[Property] = []

    class Config:
        orm_mode = True