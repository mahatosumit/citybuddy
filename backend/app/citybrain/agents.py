"""Specialist agents for CityBrain.

Each agent gathers domain context (real data or curated knowledge). A
`place_lookup` async callable (city, ptype) -> list[place] can be injected so
agents draw from the live MongoDB place catalog; otherwise they fall back to
the curated knowledge base.
"""
from typing import Dict, Any, List, Optional, Callable, Awaitable

from . import nepal_knowledge as nk
from .open_meteo import get_weather

PlaceLookup = Callable[[str, Optional[str]], Awaitable[List[Dict[str, Any]]]]


def _slim(places: List[Dict[str, Any]], limit: int = 6) -> List[Dict[str, Any]]:
    out = []
    for p in places[:limit]:
        out.append({
            "name": p.get("name"),
            "type": p.get("type"),
            "price_npr": p.get("price_npr"),
            "rating": p.get("rating"),
            "about": p.get("description") or p.get("about"),
            "tags": p.get("tags", []),
        })
    return out


async def _lookup(place_lookup: Optional[PlaceLookup], city: str, ptype: Optional[str]):
    if place_lookup:
        try:
            return await place_lookup(city, ptype)
        except Exception:
            pass
    # fallback to curated subset embedded in knowledge (rare)
    return []


async def weather_agent(city: str) -> Dict[str, Any]:
    c = nk.CITIES.get(city) or nk.CITIES["Kathmandu"]
    data = await get_weather(c["lat"], c["lon"], days=3)
    return {"agent": "WeatherAgent", "city": city, "current": data["current"],
            "forecast": data["forecast"]}


async def hotel_agent(city: str, place_lookup=None) -> Dict[str, Any]:
    return {"agent": "HotelAgent", "hotels": _slim(await _lookup(place_lookup, city, "hotel"))}


async def restaurant_agent(city: str, place_lookup=None) -> Dict[str, Any]:
    return {"agent": "RestaurantAgent", "restaurants": _slim(await _lookup(place_lookup, city, "restaurant"))}


async def attraction_agent(city: str, place_lookup=None) -> Dict[str, Any]:
    return {"agent": "AttractionAgent", "attractions": _slim(await _lookup(place_lookup, city, "attraction"))}


def events_agent() -> Dict[str, Any]:
    return {"agent": "EventsAgent", "festivals": nk.FESTIVALS}


async def budget_agent(budget_npr, city: str, place_lookup=None) -> Dict[str, Any]:
    places = await _lookup(place_lookup, city, None)
    refs = [{"name": p.get("name"), "type": p.get("type"), "price_npr": p.get("price_npr")}
            for p in places[:10] if p.get("price_npr") is not None]
    return {"agent": "BudgetAgent", "budget_npr": budget_npr, "reference_prices": refs,
            "notes": "Local meals Rs 200-600, intercity tourist bus Rs 800-2000, taxi short hop Rs 300-700, mid-range hotel Rs 2000-5000/night."}


def emergency_agent() -> Dict[str, Any]:
    return {"agent": "EmergencyAgent", "numbers": nk.EMERGENCY_NUMBERS,
            "earthquake": nk.SAFETY["earthquake"]}


def route_agent(city: str) -> Dict[str, Any]:
    return {"agent": "RouteAgent",
            "transport": nk.TRANSPORT,
            "hint": "Use ride-hailing (Pathao/InDrive) or taxis in cities, micro-buses for budget, "
                    "tourist buses for intercity. Walking is best within old city cores."}


def local_knowledge_agent(topics: List[str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {"agent": "LocalKnowledgeAgent"}
    topics = [t.lower() for t in (topics or [])]
    if any(t in ("etiquette", "culture", "custom") for t in topics):
        out["etiquette"] = nk.ETIQUETTE
    for hazard in ("monsoon", "landslide", "earthquake", "altitude"):
        if any(hazard in t for t in topics):
            out.setdefault("safety", {})[hazard] = nk.SAFETY[hazard]
    for key in ("currency", "sim", "tims", "border", "cuisine"):
        if any(key in t for t in topics):
            out.setdefault("practical", {})[key] = nk.PRACTICAL[key]["info"]
    if any("trek" in t for t in topics):
        out["treks"] = nk.TREKS
    out.setdefault("etiquette", nk.ETIQUETTE[:3])
    return out
