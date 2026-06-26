"""Real weather data via Open-Meteo (free, no API key)."""
import httpx
from typing import Dict, Any

BASE = "https://api.open-meteo.com/v1/forecast"

_WMO = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Rime fog", 51: "Light drizzle", 53: "Drizzle",
    55: "Dense drizzle", 61: "Slight rain", 63: "Rain", 65: "Heavy rain",
    66: "Freezing rain", 71: "Slight snow", 73: "Snow", 75: "Heavy snow",
    77: "Snow grains", 80: "Rain showers", 81: "Rain showers", 82: "Violent showers",
    85: "Snow showers", 86: "Snow showers", 95: "Thunderstorm",
    96: "Thunderstorm w/ hail", 99: "Severe thunderstorm",
}


def code_to_text(code) -> str:
    try:
        return _WMO.get(int(code), "Unknown")
    except (TypeError, ValueError):
        return "Unknown"


async def get_weather(lat: float, lon: float, days: int = 7) -> Dict[str, Any]:
    params = {
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,precipitation,is_day",
        "hourly": "temperature_2m,weather_code,precipitation_probability",
        "daily": "temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max,sunrise,sunset",
        "timezone": "Asia/Kathmandu", "forecast_days": days,
    }
    async with httpx.AsyncClient(timeout=20) as cx:
        r = await cx.get(BASE, params=params)
        r.raise_for_status()
        data = r.json()

    cur = data.get("current", {})
    daily = data.get("daily", {})
    hourly = data.get("hourly", {})

    forecast = []
    for i, date in enumerate(daily.get("time", [])):
        forecast.append({
            "date": date,
            "max": daily["temperature_2m_max"][i],
            "min": daily["temperature_2m_min"][i],
            "code": daily["weather_code"][i],
            "condition": code_to_text(daily["weather_code"][i]),
            "precip_prob": daily.get("precipitation_probability_max", [None] * (i + 1))[i],
        })

    hours = []
    for i, t in enumerate(hourly.get("time", [])[:24]):
        hours.append({
            "time": t,
            "temp": hourly["temperature_2m"][i],
            "code": hourly["weather_code"][i],
            "condition": code_to_text(hourly["weather_code"][i]),
            "precip_prob": hourly.get("precipitation_probability", [None] * (i + 1))[i],
        })

    return {
        "current": {
            "temp_c": cur.get("temperature_2m"),
            "feels_like_c": cur.get("apparent_temperature"),
            "humidity": cur.get("relative_humidity_2m"),
            "wind_kmh": cur.get("wind_speed_10m"),
            "precip_mm": cur.get("precipitation"),
            "is_day": bool(cur.get("is_day", 1)),
            "code": cur.get("weather_code", 0),
            "condition": code_to_text(cur.get("weather_code", 0)),
        },
        "hourly": hours,
        "forecast": forecast,
    }
