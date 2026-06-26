# CityBuddy — Product Requirements (Living Doc)

**Product:** CityBuddy — Your AI Companion for Nepal.
**Core:** "CityBrain" multi-agent AI decision engine (router -> specialist agents -> reasoned merger) grounded in real Nepal data + live weather, returning explainable structured decisions.

## Stack (adapted to environment)
- Frontend: React (CRA) + Tailwind + shadcn/ui + framer-motion + react-leaflet + TanStack Query.
- Backend: FastAPI + MongoDB (2dsphere geo). Clean feature-based modules.
- LLM: Google Gemini via Emergent key. Weather: Open-Meteo. Maps: OpenStreetMap/Leaflet.

## Phase status
- Phase 1 (POC): DONE — CityBrain proven (17/17 checks): orchestration, real weather, multilingual (EN/NE), vision, safety.
- Phase 2 (V1 app): BUILT — see below. Demo user (no auth yet).
- Phase 3: Auth (email+Google), live camera/voice, multilingual UI, PWA offline.
- Phase 4: Admin & Business dashboards, hardening, docs.

## Phase 2 features (implemented)
- CityBrain Chat (structured decisions, agent chips, reasoning accordion, history).
- Explore: Leaflet map + list, filters (type/city/search), near-me, place detail + reviews + favorites.
- AI Trip Planner (generate + save itineraries).
- Weather (live current + hourly + 7-day).
- Budget Planner (CRUD + category charts).
- Emergency Mode (numbers, nearest hospitals/police via geo, safety guidance).
- Camera AI (image upload -> Gemini vision identification).
- Nepal Intelligence hub (festivals, treks, UNESCO, transport, essentials, hazards).
- Saved (favorites + trips), Profile (preferences, AI language).
- Light/dark mode, responsive (desktop sidebar + mobile bottom tabs).

## Data
- 55 curated real Nepal places + 13 emergency POIs seeded on startup (idempotent).
