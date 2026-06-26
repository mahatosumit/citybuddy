"""CityBrain orchestrator: ROUTE -> GATHER (agents) -> MERGE.

Produces explainable, structured DECISIONS grounded in real data + Nepal
intelligence. A `place_lookup` callable can be injected to ground place agents
in the live MongoDB catalog.
"""
import json
import logging
from typing import Dict, Any, Optional, List, Callable, Awaitable

from . import agents
from . import nepal_knowledge as nk
from .llm_client import llm_json, llm_vision, extract_json, REASONING_MODEL, FAST_MODEL

logger = logging.getLogger("citybrain")

VALID_AGENTS = {
    "WeatherAgent", "HotelAgent", "RestaurantAgent", "AttractionAgent",
    "EventsAgent", "BudgetAgent", "EmergencyAgent", "RouteAgent",
    "LocalKnowledgeAgent", "TravelAgent",
}

ROUTER_SYSTEM = (
    "You are the router of CityBrain, an AI city companion for Nepal. "
    "Analyze the user's message and decide how to handle it. Respond ONLY with JSON."
)

ROUTER_PROMPT_TMPL = """User message: \"\"\"{query}\"\"\"
Known user context (may be partial): {context}

Return JSON with EXACTLY these keys:
{{
  "intent": "trip_plan | recommendation | weather | emergency | culture | safety | budget | general",
  "city": "one of {cities} or null if unknown",
  "budget_npr": number or null,
  "language": "en or ne (use ne ONLY if user wrote Nepali or asked for Nepali)",
  "topics": ["etiquette","monsoon","landslide","earthquake","altitude","currency","sim","tims","border","cuisine","trek"],
  "agents": ["subset of WeatherAgent, HotelAgent, RestaurantAgent, AttractionAgent, EventsAgent, BudgetAgent, EmergencyAgent, RouteAgent, LocalKnowledgeAgent, TravelAgent"]
}}
Pick only agents truly needed. For trip planning include TravelAgent, AttractionAgent, RestaurantAgent, RouteAgent and BudgetAgent (and HotelAgent if multi-day)."""

MERGER_SYSTEM = (
    "You are CityBrain, an elite AI city companion for Nepal that REASONS over multiple data "
    "sources (weather, places, budget, safety, culture, transport) to produce DECISIONS, not "
    "search results. You are warm, concise, practical and deeply knowledgeable about Nepal. "
    "Always ground advice in the provided agent data and Nepal context. If language is 'ne', "
    "write ALL human-readable text in natural Nepali (Devanagari). Respond ONLY with valid JSON."
)

MERGER_PROMPT_TMPL = """{nepal_context}

User asked: \"\"\"{query}\"\"\"
Output language: {language}
Agent findings (JSON): {agent_data}

Produce a JSON object with EXACTLY these keys:
{{
  "summary": "2-4 sentence direct answer / decision",
  "recommendations": [
    {{"title": "name", "detail": "why this, grounded in the data", "type": "place|tip|step|hotel|restaurant|activity", "cost_npr": number or null}}
  ],
  "reasoning": "short explanation of HOW you combined the data sources",
  "agents_used": ["agent names you actually relied on"],
  "safety_notes": ["relevant safety/weather cautions, else empty"],
  "nepal_context": "one culturally relevant Nepal note (festival/etiquette/practical), else empty",
  "confidence": "low|medium|high"
}}
Make recommendations specific and actionable; reference real place names from the agent data."""


async def _route(query: str, context: Dict[str, Any]) -> Dict[str, Any]:
    prompt = ROUTER_PROMPT_TMPL.format(
        query=query, context=json.dumps(context or {}), cities=list(nk.CITIES.keys()))
    try:
        plan = await llm_json(ROUTER_SYSTEM, prompt, model=FAST_MODEL, session_id="router")
    except Exception as e:
        logger.warning("Router failed, fallback: %s", e)
        plan = {}
    plan.setdefault("intent", "general")
    plan.setdefault("language", "en")
    plan.setdefault("topics", [])
    plan.setdefault("budget_npr", None)
    city = plan.get("city")
    if (not city or city not in nk.CITIES) and context and context.get("city") in nk.CITIES:
        city = context["city"]
    plan["city"] = city if city in nk.CITIES else "Kathmandu"
    agents_list = [a for a in plan.get("agents", []) if a in VALID_AGENTS]
    plan["agents"] = agents_list or ["LocalKnowledgeAgent"]
    return plan


async def _gather(plan: Dict[str, Any], place_lookup=None) -> Dict[str, Any]:
    city = plan["city"]
    findings: Dict[str, Any] = {}
    for a in plan["agents"]:
        try:
            if a == "WeatherAgent":
                findings[a] = await agents.weather_agent(city)
            elif a == "HotelAgent":
                findings[a] = await agents.hotel_agent(city, place_lookup)
            elif a == "RestaurantAgent":
                findings[a] = await agents.restaurant_agent(city, place_lookup)
            elif a in ("AttractionAgent", "TravelAgent"):
                findings[a] = await agents.attraction_agent(city, place_lookup)
            elif a == "EventsAgent":
                findings[a] = agents.events_agent()
            elif a == "BudgetAgent":
                findings[a] = await agents.budget_agent(plan.get("budget_npr"), city, place_lookup)
            elif a == "EmergencyAgent":
                findings[a] = agents.emergency_agent()
            elif a == "RouteAgent":
                findings[a] = agents.route_agent(city)
            elif a == "LocalKnowledgeAgent":
                findings[a] = agents.local_knowledge_agent(plan.get("topics", []))
        except Exception as e:
            logger.warning("Agent %s failed: %s", a, e)
            findings[a] = {"agent": a, "error": str(e)}
    return findings


async def process(query: str, context: Optional[Dict[str, Any]] = None,
                  place_lookup=None) -> Dict[str, Any]:
    context = context or {}
    plan = await _route(query, context)
    findings = await _gather(plan, place_lookup)
    prompt = MERGER_PROMPT_TMPL.format(
        nepal_context=nk.knowledge_brief(), query=query, language=plan["language"],
        agent_data=json.dumps(findings, ensure_ascii=False, default=str))
    result = await llm_json(MERGER_SYSTEM, prompt, model=REASONING_MODEL, session_id="merger")
    result.setdefault("agents_used", plan["agents"])
    result.setdefault("recommendations", [])
    result.setdefault("safety_notes", [])
    result.setdefault("confidence", "medium")
    result["meta"] = {"intent": plan["intent"], "city": plan["city"],
                       "language": plan["language"], "agents_invoked": plan["agents"]}
    return result


VISION_SYSTEM = (
    "You are CityBrain's Vision agent for Nepal. Identify what is in the image (landmark, temple, "
    "food dish, signboard, animal, scenery). If it is a known Nepali place or dish, name it and give "
    "rich accurate facts + a practical traveler tip. If it is text/signboard, transcribe and translate it. "
    "Respond ONLY with JSON."
)

VISION_PROMPT = """User note: {note}
Return JSON with keys:
{{
  "identification": "what this is (be specific, name it if recognizable)",
  "confidence": "high|medium|low",
  "facts": ["2-4 interesting accurate facts"],
  "traveler_tip": "one practical tip",
  "is_nepal": true/false,
  "category": "landmark|food|signboard|nature|animal|other"
}}"""


async def analyze_image(image_base64: str, note: str = "") -> Dict[str, Any]:
    raw = await llm_vision(VISION_SYSTEM, VISION_PROMPT.format(note=note or "Identify this."),
                           image_base64=image_base64, session_id="vision")
    return extract_json(raw)


TRIP_SYSTEM = (
    "You are CityBrain's Trip Planner for Nepal. Build a realistic, well-paced day-by-day itinerary "
    "grounded in the provided real places, weather and budget. Account for travel time, opening patterns, "
    "and Nepal context (festivals, etiquette, safety). Respond ONLY with valid JSON."
)

TRIP_PROMPT_TMPL = """{nepal_context}

Plan a trip with these parameters:
City/Region: {city}
Days: {days}
Budget (NPR, total, optional): {budget}
Interests: {interests}
Language: {language}

Real data available (JSON): {data}

Return JSON with EXACTLY these keys:
{{
  "title": "catchy itinerary title",
  "city": "{city}",
  "days": {days},
  "summary": "2-3 sentence overview",
  "estimated_cost_npr": number,
  "itinerary": [
    {{"day": 1, "theme": "...", "stops": [
        {{"time": "Morning", "title": "place/activity name", "detail": "what & why", "cost_npr": number, "type": "attraction|food|hotel|activity|transport"}}
    ]}}
  ],
  "tips": ["3-5 practical tips"],
  "safety_notes": ["weather/safety cautions if relevant, else empty"]
}}
Use real place names from the data. Keep each day to 3-5 stops and respect the budget if given."""


async def plan_trip(city: str, days: int, budget_npr=None, interests=None,
                    language: str = "en", place_lookup=None) -> Dict[str, Any]:
    interests = interests or []
    data = {}
    if place_lookup:
        for t in ("attraction", "restaurant", "hotel"):
            try:
                data[t + "s"] = agents._slim(await place_lookup(city, t), limit=10)
            except Exception:
                data[t + "s"] = []
    try:
        c = nk.CITIES.get(city) or nk.CITIES["Kathmandu"]
        from .open_meteo import get_weather
        w = await get_weather(c["lat"], c["lon"], days=min(int(days), 7))
        data["weather"] = {"current": w["current"], "forecast": w["forecast"]}
    except Exception:
        pass
    prompt = TRIP_PROMPT_TMPL.format(
        nepal_context=nk.knowledge_brief(), city=city, days=days,
        budget=budget_npr or "flexible", interests=", ".join(interests) or "general sightseeing",
        language=language, data=json.dumps(data, ensure_ascii=False, default=str))
    result = await llm_json(TRIP_SYSTEM, prompt, model=FAST_MODEL, session_id="trip")
    result.setdefault("city", city)
    result.setdefault("days", days)
    result.setdefault("itinerary", [])
    return result
