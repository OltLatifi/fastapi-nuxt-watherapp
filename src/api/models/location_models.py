from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, backref
from .base import Base

class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    longitude = Column(Float)
    latitude = Column(Float)
    
    forecasts = relationship('Forecast', backref='location', cascade='all, delete-orphan')

    def __repr__(self):
        return f"{self.name} | {self.latitude}x{self.longitude}"
    
class Forecast(Base):
    __tablename__ = 'forecast'

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.id'))
    weather_codes = Column(String(511))
    min_temps = Column(String(511))
    max_temps = Column(String(511))
    dates = Column(String(511))
    
    def __repr__(self):
        return f"Forecast for {self.location.name}"
