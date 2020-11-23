from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()


class RealEstate(Base):
    __tablename__ = 'real_estate'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(35), nullable=False)
    address = Column(String(150), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    properties = relationship('Property', back_populates='real_estate')

class Property(Base):
    __tablename__ = 'property'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(150), nullable=False)
    address = Column(String(150), nullable=False)
    description = Column(String(200), nullable=False)
    characteristics = Column(Text, nullable=False)
    property_type = Column(String(35), nullable=False)
    goal = Column(String(35), nullable=False)
    real_estate_id = Column(Integer, ForeignKey('real_estate.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    real_estate = relationship("RealEstate", back_populates="properties")
