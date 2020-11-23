from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func


Base = declarative_base()

class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(35), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
