"""Specialist agents for CityBrain.

Each agent gathers domain context (real data or curated knowledge) that the
CityBrain merger synthesizes into a single reasoned answer. Keeping the data
gathering deterministic (no LLM per agent) keeps latency/cost low while staying
genuinely multi-source.
"""
from typing import Dict, Any, List

import nepal_knowledge as nk
from open_meteo import get_weather


async def weather_agent(city: str) -> Dict[str, Any]:
    c = nk.CITIES.get(city) or nk.CITIES["Kathmandu"]
    data = await get_weather(c["lat"], c["lon"])
    return {"agent": "WeatherAgent", "city": city, "weather": data}


def hotel_agent(city: str) -> Dict[str, Any]:
    return {"agent": "HotelAgent", "hotels": nk.places_in_city(city, "hotel")}


def restaurant_agent(city: str) -> Dict[str, Any]:
    return {"agent": "RestaurantAgent", "restaurants": nk.places_in_city(city, "restaurant")}


def attraction_agent(city: str) -> Dict[str, Any]:
    return {"agent": "AttractionAgent", "attractions": nk.places_in_city(city, "attraction")}


def events_agent() -> Dict[str, Any]:
    return {"agent": "EventsAgent", "festivals": nk.FESTIVALS}


def budget_agent(budget_npr: float, city: str) -> Dict[str, Any]:
    places = nk.places_in_city(city)
    return {
        "agent": "BudgetAgent",
        "budget_npr": budget_npr,
        "reference_prices": [{"name": p["name"], "type": p["type"], "price_npr": p["price_npr"]} for p in places],
        "notes": "Local meals Rs 200-600, intercity bus Rs 500-1500, taxi short hop Rs 300-700.",
    }


def emergency_agent() -> Dict[str, Any]:
    return {"agent": "EmergencyAgent", "numbers": nk.EMERGENCY_NUMBERS, "earthquake": nk.SAFETY["earthquake"]}


def route_agent(city: str) -> Dict[str, Any]:
    return {"agent": "RouteAgent", "hint": "Use local taxis (negotiate or Pathao/InDrive apps), "
            "micro-buses, and tourist buses for intercity. Walking is best within old city cores."}


def local_knowledge_agent(topics: List[str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {"agent": "LocalKnowledgeAgent"}
    topics = [t.lower() for t in (topics or [])]
    if any(t in ("etiquette", "culture", "custom") for t in topics):
        out["etiquette"] = nk.ETIQUETTE
    for hazard in ("monsoon", "landslide", "earthquake", "altitude"):
        if any(hazard in t for t in topics):
            out.setdefault("safety", {})[hazard] = nk.SAFETY[hazard]
    for key in ("currency", "sim", "tims", "border"):
        if any(key in t for t in topics):
            out.setdefault("practical", {})[key] = nk.PRACTICAL[key]
    # Always provide a base etiquette+safety hint for grounding
    out.setdefault("etiquette", nk.ETIQUETTE[:3])
    return out
