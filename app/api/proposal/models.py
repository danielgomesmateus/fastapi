from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.api.client.models import Client
from app.api.property.models import Property

Base = declarative_base()


class Proposal(Base):
    __tablename__ = 'proposal'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(150), nullable=False)
    amount = Column(NUMERIC)
    client_id = Column(Integer, ForeignKey(Client.id))
    property_id = Column(Integer, ForeignKey(Property.id))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    client = relationship(Client)
    property = relationship(Property)