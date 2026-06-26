# plan.md — CityBuddy V3 Build Plan (React + FastAPI + MongoDB)

## 1) Objectives
- ✅ **Phase 1 proven:** CityBrain multi-agent orchestration + Nepal intelligence + real weather + multilingual (EN/NE) + vision all work end-to-end.
- Build a **V1 app** around the proven CityBrain core:
  - CityBrain Chat (streaming)
  - Explore Nepal places on **OpenStreetMap + Leaflet** (map + list)
  - Place detail pages
  - Trip Planner (generate + save)
  - Weather (real via Open-Meteo)
  - Budget Planner
  - Emergency Mode
  - Demo profile / demo user (Phase 2), real auth in Phase 3
- Expand into advanced intelligence + product hardening:
  - Auth (email/password + Google), per-user data
  - Camera AI UI, Voice, Offline/PWA, Events, Smart routing
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

### Phase 2 — V1 App Development (Core App around proven CityBrain; **demo user, no auth yet**) 
**Goal:** working MVP with premium UX and stable backend APIs using the proven CityBrain core.

#### Phase 2A — Design System + UX Spec (in progress)
1. Get design_agent guidelines:
   - App IA + navigation
   - Visual system (spacing, type scale, color tokens, dark mode)
   - Component patterns (chat, cards, filters, maps)
   - Mobile-first layout and accessibility AA
2. Define V1 routes/pages and interaction states:
   - Empty/loading/error states
   - Streaming chat UX
   - Map/list synchronization UX

#### Phase 2B — Backend (FastAPI + MongoDB)
1. **Port/refactor POC into backend package**:
   - Move `/app/poc/citybrain.py` → `/app/backend/app/citybrain/`
   - Convert to production structure:
     - router, merger, schemas (Pydantic), agent registry
     - LLM client wrapper (Gemini models locked)
   - Ensure consistent JSON schema + validation
2. Build feature modules (Clean Architecture / feature-based):
   - `chat`:
     - CityBrain endpoint (SSE streaming if feasible)
     - Conversation persistence (Mongo)
   - `places`:
     - hotels/restaurants/attractions/events collections
     - geo search: `$near` with **2dsphere** index
     - filters (type, price, open-now if available), pagination
     - details endpoint
   - `trips`:
     - CityBrain-generated itineraries
     - saved trips CRUD
   - `budget`:
     - budget plans CRUD
   - `weather`:
     - Open-Meteo proxy endpoint (cache where practical)
   - `emergency`:
     - Nepal emergency numbers
     - nearest hospitals/police (curated POIs + geo)
   - `reviews`, `favorites`, `profile`:
     - demo-user CRUD so flows are testable in Phase 2
3. Seed data:
   - Curated Nepal dataset (real, well-known places) import script
   - Ensure coordinate correctness + category consistency
4. Platform concerns:
   - Input validation, error handling, rate limiting (basic)
   - Logging + audit trail (basic)
   - CORS configuration

#### Phase 2C — Frontend (React + Tailwind + shadcn/ui + Framer Motion + react-leaflet)
1. App shell:
   - Responsive layout (desktop/tablet/mobile)
   - Light/dark themes
   - Accessibility AA
2. Screens:
   - Home/Landing
   - CityBrain Chat (streaming UI)
   - Explore:
     - Map + List + filters
     - “Near me” button (browser geolocation)
     - Marker clustering if needed
   - Place Detail:
     - info, map pin, hours (if known), reviews, save/favorite
   - Trip Planner:
     - generate itinerary via CityBrain, save
   - Weather
   - Budget
   - Emergency Mode
   - Profile (demo user)
3. Client data layer:
   - Query library (e.g., TanStack Query) for caching + retries
   - Robust loading/error states

**Conclude Phase 2:** run `testing_agent_v3` (backend + frontend), fix all issues.

**Phase 2 user stories (V1)**
1. Chat with CityBrain and get structured recommendations.
2. Explore places on a map, filter by type, and see nearby results.
3. Open a place detail page and read key info + reviews.
4. Generate a day itinerary and save it.
5. Open Emergency Mode and quickly see Nepal emergency numbers + nearest help.

---

### Phase 3 — Add Auth + Advanced Intelligence
**Goal:** add real user accounts + high-value intelligence features.

**Steps**
1. Auth (deferred by design):
   - Email/password (JWT) + Google OAuth
   - RBAC roles: user, business, admin
   - Migrate demo data → per-user collections
   - Document test bypass credentials/workflows
2. Camera AI UI (Vision):
   - upload/capture → identify landmark/food/translate signboard
   - backed by Gemini vision (`VISION_MODEL=gemini-2.5-flash`)
3. Multilingual:
   - UI language toggle EN/NE
   - CityBrain/Translation agent supports Nepali output reliably
4. Voice assistant:
   - Web Speech API input + TTS output (where supported)
5. Events + festival calendar:
   - Dashain/Tihar/Holi/Indra Jatra/Losar integration
   - smarter routing (multi-stop optimization via CityBrain + map)
6. PWA Offline Mode:
   - cache core screens + seed data

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
2. **Get design_agent output** and lock the UI architecture for Phase 2.
3. Start Phase 2 backend:
   - port `/app/poc/` into `/app/backend/app/citybrain/`
   - implement core endpoints + Mongo schema + seed importer
4. Start Phase 2 frontend:
   - app shell + chat streaming UI + Explore map/list

---

## 4) Success Criteria
- ✅ Phase 1: `test_core.py` passes all scenarios (17/17) with strict JSON, real weather, Nepali output, and working vision.
- Phase 2: V1 app supports chat + map exploration + details + trip/budget/emergency flows with stable APIs (demo user).
- Phase 3: Auth (email+Google) works; vision/voice/multilingual/offline features function end-to-end.
- Phase 4: Admin/business dashboards functional; security/perf/accessibility validated; deployment documented.
