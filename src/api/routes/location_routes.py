from sqlalchemy import func
from errors.client_exceptions import ClientGatewayException
from utils import save, to_dict
from client.forecast import forecast
from schemas.location_requests import LocationCreate
from schemas.location_responses import LocationRead
from models.location_models import Location, Forecast
from models.city_model import City
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from connection import get_db
from schemas.location_responses import CityRead, LocationResponse

from client.meteo_scraper import get_forecast


router = APIRouter(
    prefix="/locations",
    tags=["locations"],
)

@router.get("/")
async def get_locations(db: Session = Depends(get_db)) -> list[LocationResponse]:
    subquery = db.query(
        Forecast.location_id,
        func.max(Forecast.id).label('last_forecast_id')
    ).group_by(Forecast.location_id).subquery()

    query = db.query(Location, Forecast).join(
        subquery, Location.id == subquery.c.location_id
    ).join(
        Forecast, Forecast.id == subquery.c.last_forecast_id
    )

    return [{"location": location, "forecast": forecast} for (location, forecast) in query.all()]
        
        
@router.post("/")
async def create_location(body: LocationCreate, db: Session = Depends(get_db)) -> LocationResponse:
    location = Location(
        name=body.name,
        latitude=body.latitude,
        longitude=body.longitude
    )
    await save(location, db)
    location_data: LocationRead = to_dict(location)
    weather_data: Forecast = await forecast(body.latitude, body.longitude)


    forecast_obj = Forecast(
        location_id=location.id,
        **weather_data
    )

    await save(forecast_obj, db)

    processed_location: LocationResponse = {
        "location": location_data,
        "forecast": weather_data
    }

    return processed_location

@router.delete("/{id}")
async def delete_location(id: int, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == id).first()

    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    db.delete(location)
    db.commit()

    return {"message": "Location deleted successfully"}

@router.get("/cities")
async def get_cities(db: Session = Depends(get_db)) -> list[CityRead]:
    return db.query(City).all()

@router.get("/cron")
async def cron(db: Session = Depends(get_db)):
    locations = db.query(Location).all()
    try:
        await get_forecast(db, locations)
    except ClientGatewayException as e:
        print("error ->", e)
        return "Error"
    return "Success"

