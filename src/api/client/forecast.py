from errors.client_exceptions import ClientGatewayException
import httpx

from models.location_models import Forecast

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

async def forecast(latitude: float, longitude: float) -> Forecast:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": "auto",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(OPEN_METEO_URL, params=params)
            response.raise_for_status()

        data = response.json()

        daily = data["daily"]

        weather_codes = [str(weather_code) for weather_code in daily['weather_code']]
        min_temps = [str(min_temp) for min_temp in daily['temperature_2m_min']]
        max_temps = [str(max_temp) for max_temp in daily['temperature_2m_max']]
        dates = [str(date) for date in daily['time']]

        response_data = {
            "dates": ",".join(dates),
            "max_temps": ",".join(max_temps),
            "min_temps": ",".join(min_temps),
            "weather_codes": ",".join(weather_codes)
        }

        return response_data

    except Exception as e:
        print("error ->", e)
        raise ClientGatewayException(f"An error occurred: {e}")