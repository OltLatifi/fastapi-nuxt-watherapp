from utils import get_last_forecast
from models.location_models import Location
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from connection import get_db
from schemas.location_responses import Forecast


router = APIRouter(
    prefix="/forecast",
    tags=["forecast"]
)


@router.get("/{id}")
async def get_forecast(id:int, db: Session = Depends(get_db)) -> Forecast:
    location = db.query(Location).filter(Location.id == id).first()

    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    
    forecast = await get_last_forecast(db, location.id)

    return forecast