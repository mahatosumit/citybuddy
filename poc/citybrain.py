"""CityBrain - the central reasoning/orchestration engine.

Flow:
  1. ROUTE  (fast LLM): classify intent, extract city/budget/language/topics,
            and decide which specialist agents to invoke.
  2. GATHER (deterministic agents): collect real data + curated knowledge.
  3. MERGE  (reasoning LLM): synthesize a single structured, reasoned answer.

Vision queries take a dedicated multimodal path.
"""
import json
import logging
from typing import Dict, Any, Optional, List

import agents
import nepal_knowledge as nk
from llm_client import llm_json, llm_text, llm_vision, REASONING_MODEL, FAST_MODEL

logger = logging.getLogger("citybrain")

VALID_AGENTS = {
    "WeatherAgent", "HotelAgent", "RestaurantAgent", "AttractionAgent",
    "EventsAgent", "BudgetAgent", "EmergencyAgent", "RouteAgent",
    "LocalKnowledgeAgent", "TravelAgent",
}

ROUTER_SYSTEM = (
    "You are the router of CityBrain, an AI city companion for Nepal. "
    "Analyze the user's message and decide how to handle it. "
    "Respond ONLY with a JSON object, no prose."
)

ROUTER_PROMPT_TMPL = """User message: \"\"\"{query}\"\"\"
Known user context (may be partial): {context}

Return JSON with EXACTLY these keys:
{{
  "intent": "trip_plan | recommendation | weather | emergency | culture | safety | budget | general",
  "city": "one of {cities} or null if unknown",
  "budget_npr": number or null,
  "language": "en or ne (use ne ONLY if the user wrote in Nepali or asked for Nepali)",
  "topics": ["etiquette", "monsoon", "landslide", "earthquake", "altitude", "currency", "sim", "tims", "border"],
  "agents": ["subset of: WeatherAgent, HotelAgent, RestaurantAgent, AttractionAgent, EventsAgent, BudgetAgent, EmergencyAgent, RouteAgent, LocalKnowledgeAgent, TravelAgent"]
}}
Pick only the agents truly needed. For trip planning include TravelAgent, AttractionAgent, RestaurantAgent, RouteAgent and BudgetAgent if a budget is mentioned."""

MERGER_SYSTEM = (
    "You are CityBrain, an elite AI city companion for Nepal that REASONS over multiple "
    "data sources (weather, places, budget, safety, culture) to produce DECISIONS, not search "
    "results. You are warm, concise, practical and deeply knowledgeable about Nepal. "
    "Always ground advice in the provided agent data and Nepal context. "
    "If language is 'ne', write all human-readable text in natural Nepali (Devanagari). "
    "Respond ONLY with a valid JSON object."
)

MERGER_PROMPT_TMPL = """{nepal_context}

User asked: \"\"\"{query}\"\"\"
Output language: {language}
Agent findings (JSON): {agent_data}

Produce a JSON object with EXACTLY these keys:
{{
  "summary": "2-4 sentence direct answer / decision",
  "recommendations": [
    {{"title": "name", "detail": "why this, grounded in the data", "type": "place|tip|step|hotel|restaurant|activity"}}
  ],
  "reasoning": "short explanation of HOW you combined the data sources to decide",
  "agents_used": ["list of agent names you actually relied on"],
  "safety_notes": ["any relevant safety/weather caution, else empty list"],
  "nepal_context": "one culturally relevant Nepal-specific note (festival/etiquette/practical), else empty string"
}}
Make recommendations specific and actionable. Reference real place names from the agent data when available."""


async def _route(query: str, context: Dict[str, Any]) -> Dict[str, Any]:
    prompt = ROUTER_PROMPT_TMPL.format(
        query=query,
        context=json.dumps(context or {}),
        cities=list(nk.CITIES.keys()),
    )
    try:
        plan = await llm_json(ROUTER_SYSTEM, prompt, model=FAST_MODEL, session_id="router")
    except Exception as e:
        logger.warning("Router failed, using fallback: %s", e)
        plan = {}
    # Normalize
    plan.setdefault("intent", "general")
    plan.setdefault("language", "en")
    plan.setdefault("topics", [])
    plan.setdefault("budget_npr", None)
    city = plan.get("city")
    if context and context.get("city") and not city:
        city = context["city"]
    if city not in nk.CITIES:
        city = city if city in nk.CITIES else None
    plan["city"] = city or "Kathmandu"
    agents_list = [a for a in plan.get("agents", []) if a in VALID_AGENTS]
    if not agents_list:
        agents_list = ["LocalKnowledgeAgent"]
    plan["agents"] = agents_list
    return plan


async def _gather(plan: Dict[str, Any]) -> Dict[str, Any]:
    city = plan["city"]
    findings: Dict[str, Any] = {}
    for a in plan["agents"]:
        try:
            if a == "WeatherAgent":
                findings[a] = await agents.weather_agent(city)
            elif a == "HotelAgent":
                findings[a] = agents.hotel_agent(city)
            elif a == "RestaurantAgent":
                findings[a] = agents.restaurant_agent(city)
            elif a in ("AttractionAgent", "TravelAgent"):
                findings[a] = agents.attraction_agent(city)
            elif a == "EventsAgent":
                findings[a] = agents.events_agent()
            elif a == "BudgetAgent":
                findings[a] = agents.budget_agent(plan.get("budget_npr"), city)
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


async def process(query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    context = context or {}
    plan = await _route(query, context)
    findings = await _gather(plan)
    prompt = MERGER_PROMPT_TMPL.format(
        nepal_context=nk.knowledge_brief(),
        query=query,
        language=plan["language"],
        agent_data=json.dumps(findings, ensure_ascii=False, default=str),
    )
    result = await llm_json(MERGER_SYSTEM, prompt, model=REASONING_MODEL, session_id="merger")
    # Attach orchestration metadata
    result["_plan"] = {"intent": plan["intent"], "city": plan["city"],
                       "language": plan["language"], "agents_invoked": plan["agents"]}
    result.setdefault("agents_used", plan["agents"])
    return result


VISION_SYSTEM = (
    "You are CityBrain's Vision agent for Nepal. Identify what is in the image "
    "(landmark, temple, food dish, signboard, animal, scenery). If it is a known Nepali "
    "place or dish, name it and give a few rich, accurate facts + a practical traveler tip. "
    "If it is text/signboard, transcribe and translate it. Respond ONLY with JSON."
)

VISION_PROMPT = """User note: {note}
Return JSON with keys:
{{
  "identification": "what this is (be specific, name it if recognizable)",
  "confidence": "high|medium|low",
  "facts": ["2-4 interesting, accurate facts"],
  "traveler_tip": "one practical tip",
  "is_nepal": true/false
}}"""


async def analyze_image(image_base64: str, note: str = "") -> Dict[str, Any]:
    raw = await llm_vision(VISION_SYSTEM, VISION_PROMPT.format(note=note or "Identify this."),
                            image_base64=image_base64, session_id="vision")
    from llm_client import _extract_json
    return _extract_json(raw)
