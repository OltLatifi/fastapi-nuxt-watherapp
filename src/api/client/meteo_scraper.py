from errors.client_exceptions import ClientGatewayException
from sqlalchemy.orm import Session
import httpx

from models.location_models import Forecast, Location

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

async def get_forecast(db: Session, locations: list[Location]) -> dict | None:
    if len(locations) == 0:
        return None
    
    latitudes = [str(location.latitude) for location in locations]
    longitudes = [str(location.longitude) for location in locations]

    params = {
        "latitude": ','.join(latitudes),
        "longitude": ','.join(longitudes),
        "timezone": "auto",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(OPEN_METEO_URL, params=params)
            response.raise_for_status()
            data = response.json()
    except Exception as e:
        print("error ->", e)
        raise ClientGatewayException(e)
        

    for index, location in enumerate(locations):
        if type(data) is list:
            client_data = data[index]["daily"]
        else:
            client_data = data["daily"]

        weather_codes = [str(weather_code) for weather_code in client_data['weather_code']]
        min_temps = [str(min_temp) for min_temp in client_data['temperature_2m_min']]
        max_temps = [str(max_temp) for max_temp in client_data['temperature_2m_max']]
        dates = [str(date) for date in client_data['time']]

        forecast = Forecast(
            location_id=location.id,
            weather_codes=",".join(weather_codes),
            min_temps=",".join(min_temps),
            max_temps=",".join(max_temps),
            dates=",".join(dates),
        )
        db.add(forecast)
    db.commit()