"""CityBrain POC — single end-to-end test script.

Validates the hardest parts of CityBuddy in isolation BEFORE building the app:
  1. LLM connectivity (Gemini fast + reasoning models via Emergent key)
  2. Multi-agent trip planning (structured, reasoned, budget-aware, real places)
  3. Weather + activity reasoning (REAL Open-Meteo data)
  4. Nepali-language response (Devanagari)
  5. Safety / monsoon guidance
  6. Vision agent (identify a real Nepal landmark from an image)

Run: python test_core.py
"""
import asyncio
import json
import re
import sys

import httpx

import citybrain
from llm_client import llm_text, FAST_MODEL, REASONING_MODEL, bytes_to_b64

PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"

results = []


def check(name, cond, info=""):
    status = PASS if cond else FAIL
    results.append((name, bool(cond)))
    print(f"  [{status}] {name}" + (f" — {info}" if info else ""))
    return cond


def has_devanagari(text: str) -> bool:
    return bool(re.search(r"[\u0900-\u097F]", text or ""))


async def test_llm_connectivity():
    print("\n=== TEST 1: LLM connectivity (both Gemini tiers) ===")
    try:
        fast = await llm_text("You are a test.", "Reply with exactly: OK_FAST", model=FAST_MODEL)
        check("Fast model responds", "OK_FAST" in fast.upper(), f"{FAST_MODEL}: {fast.strip()[:40]}")
    except Exception as e:
        check("Fast model responds", False, str(e))
    try:
        reasoning = await llm_text("You are a test.", "Reply with exactly: OK_PRO", model=REASONING_MODEL)
        check("Reasoning model responds", "OK_PRO" in reasoning.upper(), f"{REASONING_MODEL}: {reasoning.strip()[:40]}")
    except Exception as e:
        check("Reasoning model responds", False, str(e))


async def test_trip_plan():
    print("\n=== TEST 2: Budget trip plan (multi-agent orchestration) ===")
    res = await citybrain.process(
        "Plan a 2-day budget trip in Pokhara under NPR 5000. I love nature and lakes.",
        context={"city": "Pokhara"},
    )
    print(json.dumps(res, ensure_ascii=False, indent=2)[:1400])
    check("Returns summary", bool(res.get("summary")))
    check("Returns recommendations", isinstance(res.get("recommendations"), list) and len(res["recommendations"]) >= 2,
          f"{len(res.get('recommendations', []))} recs")
    check("Returns reasoning", bool(res.get("reasoning")))
    used = res.get("agents_used", [])
    check("Used multiple agents", len(used) >= 2, ", ".join(used))
    blob = json.dumps(res, ensure_ascii=False).lower()
    check("Grounded in real Pokhara places", any(p in blob for p in ["phewa", "sarangkot", "world peace", "lakeside"]))
    check("Routed to Pokhara", res.get("_plan", {}).get("city") == "Pokhara")


async def test_weather_activity():
    print("\n=== TEST 3: Weather + activity reasoning (REAL Open-Meteo) ===")
    res = await citybrain.process("What's the weather in Kathmandu right now and what should I do today?")
    print(json.dumps(res, ensure_ascii=False, indent=2)[:1200])
    used = res.get("agents_used", [])
    plan_agents = res.get("_plan", {}).get("agents_invoked", [])
    check("WeatherAgent invoked", "WeatherAgent" in used or "WeatherAgent" in plan_agents, ", ".join(plan_agents))
    check("Has actionable summary", bool(res.get("summary")))
    check("Has recommendations", len(res.get("recommendations", [])) >= 1)


async def test_weather_raw():
    print("\n=== TEST 3b: Open-Meteo returns real numeric data ===")
    from open_meteo import get_weather
    from nepal_knowledge import CITIES
    c = CITIES["Kathmandu"]
    w = await get_weather(c["lat"], c["lon"])
    temp = w["current"]["temp_c"]
    check("Current temp is a real number", isinstance(temp, (int, float)), f"{temp}°C, {w['current']['condition']}")
    check("3-day forecast present", len(w["forecast"]) >= 3, f"{len(w['forecast'])} days")


async def test_nepali():
    print("\n=== TEST 4: Nepali-language cultural response ===")
    res = await citybrain.process("कृपया नेपाली संस्कृति र मन्दिरमा पालना गर्नुपर्ने नियमहरू नेपालीमा बताउनुहोस्।")
    txt = json.dumps(res, ensure_ascii=False)
    print(json.dumps(res, ensure_ascii=False, indent=2)[:1000])
    check("Detected Nepali language", res.get("_plan", {}).get("language") == "ne", res.get("_plan", {}).get("language"))
    check("Response contains Devanagari", has_devanagari(txt))


async def test_safety():
    print("\n=== TEST 5: Monsoon / safety guidance ===")
    res = await citybrain.process("I'm driving Kathmandu to Pokhara in monsoon season. Any safety advice?")
    blob = json.dumps(res, ensure_ascii=False).lower()
    print(json.dumps(res, ensure_ascii=False, indent=2)[:1000])
    check("Has safety notes or safety content",
          (len(res.get("safety_notes", [])) >= 1) or any(k in blob for k in ["landslide", "monsoon", "rain", "road"]))


async def _download_image():
    import os
    import subprocess
    local = os.path.join(os.path.dirname(__file__), "boudhanath_test.jpg")
    if os.path.exists(local) and os.path.getsize(local) > 5000:
        with open(local, "rb") as f:
            return f.read()
    # Fallback: fetch via curl (Wikimedia blocks some clients)
    url = "https://commons.wikimedia.org/wiki/Special:FilePath/Boudhanath.jpg?width=640"
    try:
        subprocess.run(["curl", "-s", "-L", "-A", "Mozilla/5.0 (CityBuddy)", "-o", local, url], check=True, timeout=40)
        if os.path.exists(local) and os.path.getsize(local) > 5000:
            with open(local, "rb") as f:
                return f.read()
    except Exception:
        pass
    return None


async def test_vision():
    print("\n=== TEST 6: Vision agent identifies a Nepal landmark ===")
    img = await _download_image()
    if not img:
        check("Image downloaded for vision test", False, "could not fetch test image")
        return
    b64 = bytes_to_b64(img)
    res = await citybrain.analyze_image(b64, note="Where in Nepal is this and what is it?")
    print(json.dumps(res, ensure_ascii=False, indent=2)[:900])
    ident = (res.get("identification", "") or "").lower()
    check("Vision returned identification", bool(ident))
    check("Recognized as Nepal / stupa", res.get("is_nepal") is True or any(
        k in ident for k in ["stupa", "boudha", "boudhanath", "buddhist", "nepal", "kathmandu"]))
    check("Provided facts", isinstance(res.get("facts"), list) and len(res["facts"]) >= 1)


async def main():
    print("=" * 64)
    print("CITYBRAIN CORE POC — END TO END VALIDATION")
    print("=" * 64)
    await test_llm_connectivity()
    await test_weather_raw()
    await test_trip_plan()
    await test_weather_activity()
    await test_nepali()
    await test_safety()
    await test_vision()

    print("\n" + "=" * 64)
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    for name, ok in results:
        print(f"  {'OK ' if ok else 'XX '} {name}")
    print(f"\nRESULT: {passed}/{total} checks passed")
    print("=" * 64)
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    asyncio.run(main())
