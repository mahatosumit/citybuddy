"""Weather endpoint (real Open-Meteo data)."""
from typing import Optional
from fastapi import APIRouter, HTTPException

from ..citybrain.open_meteo import get_weather
from ..citybrain.nepal_knowledge import CITIES

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("")
async def weather(city: Optional[str] = None, lat: Optional[float] = None,
                  lon: Optional[float] = None, days: int = 7):
    if lat is None or lon is None:
        c = CITIES.get(city or "Kathmandu") or CITIES["Kathmandu"]
        lat, lon = c["lat"], c["lon"]
        resolved_city = city if city in CITIES else "Kathmandu"
    else:
        resolved_city = city or "Current location"
    try:
        data = await get_weather(lat, lon, days=min(max(days, 1), 7))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Weather service error: {e}")
    data["city"] = resolved_city
    data["lat"], data["lon"] = lat, lon
    return data


@router.get("/cities")
async def weather_cities():
    return [{"city": k, **v} for k, v in CITIES.items()]
