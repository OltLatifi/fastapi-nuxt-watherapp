from sqlalchemy.orm import Session
from connection import get_db
from models.city_model import City
from static_data import country_data

def seed_data(db: Session):
    for data in country_data:
        city = City(
            name=data["Capital City"],
            country=data["Country"],
            longitude=data["Longitude"],
            latitude=data["Latitude"],
        )
        db.add(city)
    db.commit()

db = next(get_db()) 

try:
    seed_data(db)
finally:
    db.close()
