from pydantic import BaseModel
from .location_requests import LocationCreate

class LocationRead(LocationCreate):
    id: int


class Forecast(BaseModel):
    dates: str
    weather_codes: str
    min_temps: str
    max_temps: str


class LocationResponse(BaseModel):
    location: LocationRead
    forecast: Forecast


class CityRead(BaseModel):
    id: int
    name: str
    country: str
    longitude: float
    latitude: float