# plan.md — CityBuddy V3 Build Plan (React + FastAPI + MongoDB)

## 1) Objectives
- ✅ **Phase 1 proven:** CityBrain multi-agent orchestration + Nepal intelligence + real weather + multilingual (EN/NE) + vision all work end-to-end.
- ✅ **Phase 2 delivered:** a polished **V1 app** around the proven CityBrain core:
  - CityBrain Chat (structured decisions + reasoning)
  - Explore Nepal places on **OpenStreetMap + Leaflet** (map + list + filters)
  - Place detail pages (reviews + nearby + mini-map)
  - Trip Planner (AI generate + save)
  - Weather (real via Open-Meteo)
  - Budget Planner (CRUD + charts)
  - Emergency Mode (numbers + nearby facilities + guidance)
  - Nepal Intelligence hub
  - Camera AI (image upload → Gemini vision)
  - Demo profile / demo user (Phase 2), real auth in Phase 3
- Expand into advanced intelligence + product hardening:
  - Auth (email/password + Google), true per-user data
  - Live camera capture, Voice, Offline/PWA
  - Events/festival expansion + smarter routing
  - Admin + Business dashboards, security/observability, release readiness

---

## 2) Implementation Steps

### Phase 1 — Core POC (CityBrain in Isolation) ✅ **COMPLETE**
**Goal:** a single `test_core.py` script that validates integrations + orchestration end-to-end.

**What was built (in `/app/poc/`)**
- `llm_client.py`
  - **LOCKED** Google Gemini via Emergent key
  - `FAST_MODEL=gemini-2.5-flash`
  - `REASONING_MODEL=gemini-3.1-pro-preview`
  - `VISION_MODEL=gemini-2.5-flash`
  - JSON output via `response_format={"type":"json_object"}`
  - Vision via `ImageContent` (base64)
- `citybrain.py`
  - Router → deterministic specialist agents → reasoning merger
  - Strict structured JSON output:
    - `{summary, recommendations[], reasoning, agents_used, safety_notes, nepal_context, _plan}`
- `agents.py`, `open_meteo.py`, `nepal_knowledge.py`
  - Real Open-Meteo weather
  - Curated Nepal intelligence + real place seed subset
- `test_core.py`
  - End-to-end validation script

**Result:** `test_core.py` passes **17/17 checks**:
- Gemini fast + reasoning models work via Emergent key
- Multi-agent orchestration returns strict structured JSON
- Real weather confirmed (Kathmandu live temp + 3-day forecast)
- Budget trip planning grounded in real Pokhara places (Phewa, Sarangkot, World Peace Pagoda, Hotel Lakeside, Or2k)
- Nepali/Devanagari responses confirmed (`language='ne'` auto-detected)
- Monsoon/landslide safety guidance confirmed
- Vision confirmed: correctly identified **Boudhanath Stupa** with accurate facts + traveler tip

**Phase 1 user stories (POC) — Completed**
1. ✅ “Plan a 2-day budget trip in Pokhara under NPR 5000” → structured, reasoned plan.
2. ✅ “What’s the weather in Kathmandu and what should I do today?” → weather + activities.
3. ✅ Nepali etiquette question → correct Nepali/Devanagari output.
4. ✅ Vision: landmark identification from image.
5. ✅ Monsoon/landslide safety advice.

---

### Phase 2 — V1 App Development (Core App around proven CityBrain; **demo user, no auth yet**) ✅ **COMPLETE**
**Goal:** working MVP with premium UX and stable backend APIs using the proven CityBrain core.

#### Phase 2A — Design System + UX Spec ✅ **COMPLETE**
1. ✅ Design guidelines generated in `/app/design_guidelines.md`:
   - IA + navigation (desktop sidebar, mobile bottom tabs)
   - Visual system (type scale, spacing, color tokens, light/dark)
   - Component patterns (chat decisions, map+list explore, cards, emergency)
   - Accessibility AA guidance
2. ✅ V1 routes/pages and interaction states defined and implemented:
   - Empty/loading/error states
   - Agent chips + “Why this” accordion
   - Responsive layouts across desktop/tablet/mobile

#### Phase 2B — Backend (FastAPI + MongoDB) ✅ **COMPLETE**
**Implemented under:** `/app/backend/app` with feature routers mounted at `/api`.

1. ✅ **Port/refactor POC into backend CityBrain package**:
   - `/app/backend/app/citybrain/`:
     - `llm_client.py`, `nepal_knowledge.py`, `open_meteo.py`, `agents.py`, `orchestrator.py`
   - CityBrain grounding via `place_lookup` injection to use the live MongoDB catalog
   - Strict JSON schemas returned by AI endpoints

2. ✅ Feature modules (feature-based routers):
   - `chat`:
     - `POST /api/chat/message` (CityBrain decisions)
     - conversation persistence (`/api/chat/conversations`, get/delete)
   - `places`:
     - `GET /api/places` filters (type/city/q) + geo search (`$near`) with **2dsphere** index
     - `GET /api/places/cities`, `GET /api/places/{id}` (includes nearby + review stats)
   - `trips`:
     - `POST /api/trips/generate` (AI itinerary)
     - saved trips CRUD (`GET/POST/GET{id}/DELETE`)
   - `budget`:
     - budgets CRUD (`GET/POST/PUT/DELETE`)
   - `weather`:
     - `GET /api/weather` proxy to Open-Meteo (current + hourly + forecast)
   - `emergency`:
     - `GET /api/emergency/numbers`
     - `GET /api/emergency/nearby` (geo)
     - `GET /api/emergency/guidance-all`
   - `nepal`:
     - `/api/nepal/festivals`, `/treks`, `/unesco`, `/transport`, `/info`, `/overview`
   - `vision`:
     - `POST /api/vision/analyze` (Gemini multimodal)
   - `reviews`, `favorites`, `profile`:
     - demo-user CRUD for Phase 2 flows

3. ✅ Seed data:
   - Idempotent seeding on startup
   - **55 curated real Nepal places** + **13 emergency POIs**
   - Stored with GeoJSON Point `{type:"Point", coordinates:[lon,lat]}`

4. ✅ Platform concerns:
   - Input validation + error handling
   - CORS enabled
   - Core indexes created on startup

5. ✅ Known behavior (not a bug):
   - `POST /api/trips/generate` can take ~30–40s depending on model output size.

#### Phase 2C — Frontend (React + Tailwind + shadcn/ui + Framer Motion + react-leaflet) ✅ **COMPLETE**
**Implemented under:** `/app/frontend/src`.

1. ✅ App shell:
   - Desktop sidebar + mobile bottom tabs
   - Topbar: theme toggle + AI-language toggle
   - Light/dark mode, premium styling and motion

2. ✅ Screens/pages:
   - Home (hero + quick actions + cities + top-rated places)
   - CityBrain Chat (structured decisions, agent chips, “Why this” accordion, history)
   - Explore (Leaflet map + list, type/city/search filters, near-me, favorites)
   - Place Detail (overview + reviews + add review, mini-map, nearby)
   - Trip Planner (AI itinerary generate + save; improved loading message)
   - Weather (current + hourly + 7-day)
   - Budget (CRUD + pie/progress charts)
   - Emergency (call cards + nearest facilities + safety guidance tabs)
   - Camera AI (image upload → vision results)
   - Nepal Intelligence hub (tabs: festivals/treks/heritage/transport/essentials)
   - Saved (favorites + saved trips)
   - Profile (preferences + language)

3. ✅ Client data layer:
   - `axios` API client in `/src/lib/api.js`
   - TanStack Query for caching/retries/loading states

4. ✅ Fix applied during build:
   - JSX unicode escape sequences were rendering literally; replaced with real characters across frontend.

#### Phase 2 Testing ✅ **COMPLETE**
- `testing_agent_v3` report (iteration_1):
  - Backend: **35/37 (94.6%)**
  - Frontend: **100%** (all tested features working)
  - Overall: **97%**
  - **Zero critical/UI/integration/design bugs**
  - Only note: trip-generation latency (expected AI workload); loader UX improved.

**Phase 2 user stories (V1) — Completed**
1. ✅ Chat with CityBrain and get structured recommendations.
2. ✅ Explore places on a map, filter by type/city, and see nearby results.
3. ✅ Open a place detail page and read key info + reviews.
4. ✅ Generate a day-by-day itinerary and save it.
5. ✅ Open Emergency Mode and quickly see Nepal emergency numbers + nearest help.

---

### Phase 3 — Add Auth + Advanced Intelligence (NEXT)
**Goal:** add real user accounts + advanced intelligence features and app-like capabilities.

**Steps**
1. Auth (replace demo user):
   - Email/password (JWT) + Google OAuth
   - RBAC roles: user, business, admin
   - Migrate demo flows to per-user security
   - Document test bypass credentials/workflows
2. Upgrade chat experience:
   - Optional SSE streaming endpoint + streaming UI (if needed)
   - Persist full assistant decision payloads and support multi-turn memory
3. Live Camera capture:
   - Add in-browser camera capture (getUserMedia) in Camera AI page
   - Continue to support file upload fallback
4. Multilingual:
   - Full UI language toggle EN/NE (not just AI output)
   - Ensure CityBrain outputs Nepali consistently when selected
5. Voice assistant:
   - Web Speech API for voice input (fallback to typing)
   - Optional TTS for responses
6. Events + festival calendar expansion:
   - Expand events dataset; surface by city/time
   - Smarter routing: multi-stop route + travel time heuristics
7. PWA Offline Mode:
   - Service worker + caching for core routes and seed data

**Conclude Phase 3:** run `testing_agent_v3`, fix all issues.

**Phase 3 user stories**
1. Sign up/login (email + Google) and keep saved trips/favorites.
2. Take/upload a photo of a landmark and get identification + tips.
3. Switch the app to Nepali UI and get Nepali AI responses.
4. Speak a query and receive a spoken response.
5. Build a multi-stop route and get an optimized plan.

---

### Phase 4 — Dashboards, Hardening, Release Readiness
**Goal:** admin/business tooling + production hardening.

**Steps**
1. Admin dashboard:
   - manage places, reviews, users
   - seed data editor and import tooling
2. Business dashboard:
   - claim listing, edit info, respond to reviews
3. Security hardening:
   - OWASP checks, stricter rate limiting
   - audit trails
   - backup strategy
4. Observability:
   - structured logs, health checks
5. Final perf/accessibility pass; docs:
   - README, API docs, deployment guide

**Conclude Phase 4:** run `testing_agent_v3`, fix all issues.

**Phase 4 user stories**
1. Admin can add/edit/remove places and see updates on the map.
2. Business owner can claim listing and update hours/photos.
3. Admin can moderate reviews.
4. App stays fast and accessible on mobile.
5. Deploy via Docker and verify health checks.

---

## 3) Next Actions (Immediate)
1. ✅ Phase 1 complete: CityBrain POC validated; models locked to Gemini (fast/reasoning/vision).
2. ✅ Phase 2 complete: V1 app delivered + tested; curated Nepal dataset seeded.
3. Next: Begin Phase 3 when ready:
   - Implement auth (email/password + Google) and replace demo user flows
   - Add live camera capture + voice
   - Expand events + PWA offline

---

## 4) Success Criteria
- ✅ Phase 1: `test_core.py` passes all scenarios (17/17) with strict JSON, real weather, Nepali output, and working vision.
- ✅ Phase 2: V1 app supports chat + map exploration + details + trip/budget/emergency flows with stable APIs (demo user), premium UI, and successful end-to-end tests.
- Phase 3: Auth (email+Google) works; live camera/voice/multilingual UI/offline features function end-to-end.
- Phase 4: Admin/business dashboards functional; security/perf/accessibility validated; deployment documented.
