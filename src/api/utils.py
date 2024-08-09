from sqlalchemy import desc
from sqlalchemy.orm import Session

from models.location_models import Forecast

from sqlalchemy.ext.declarative import DeclarativeMeta

def to_dict(instance):
    data = {column.name: getattr(instance, column.name)
            for column in instance.__table__.columns}
    return data


async def save(model, db: Session):
    db.add(model)
    db.commit()
    db.refresh(model)

async def get_last_forecast(db: Session, location_id: int) -> Forecast | None:
    return db.query(Forecast).filter(
        Forecast.location_id == location_id
    ).order_by(desc(Forecast.id)).first()