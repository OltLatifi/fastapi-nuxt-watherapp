from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from .base import Base

class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    country = Column(String(255))
    longitude = Column(Float)
    latitude = Column(Float)
    
    def __repr__(self):
        return f"{self.name}"