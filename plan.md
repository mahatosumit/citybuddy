# plan.md — CityBuddy V3 Build Plan (React + FastAPI + MongoDB)

## 1) Objectives
- Prove the **core workflow** works: CityBrain multi-agent orchestration + Nepal intelligence + weather + multilingual + vision.
- Build a **V1 app** around the proven core: chat + explore (map/list) + place details + trips + budget + emergency.
- Expand into advanced intelligence (vision UI, voice, offline/PWA, events, routing) and then dashboards.

---

## 2) Implementation Steps

### Phase 1 — Core POC (CityBrain in Isolation) ✅ *Must pass before app build*
**Goal:** a single `test_core.py` script that validates integrations + orchestration end-to-end.

**Steps**
1. Websearch best practices for:
   - Gemini/Gemma access via Emergent key (model availability), structured JSON outputs, and vision calls.
   - Lightweight agent orchestration patterns in Python (router + tool/agent registry).
2. Create minimal Python modules:
   - `llm_client.py` (Emergent LLM wrapper; verify “Gemma” availability, fallback to Google Gemini if needed)
   - `citybrain.py` (router → agents → merger; returns strict JSON)
   - `agents/` (Travel/Hotel/Restaurant/Weather/Route/Budget/Emergency/Events/Vision/Translation/LocalKnowledge)
   - `nepal_knowledge.py` (festivals/etiquette/safety/trek/monsoon/earthquake guidance snippets)
   - `open_meteo.py` (real API call)
3. Implement `test_core.py` covering user stories (below) and asserting:
   - Response JSON schema: `{summary, recommendations[], reasoning, agents_used, safety_notes?, sources?}`
   - Nepal-specific context appears when relevant
   - Weather is real (Open-Meteo)
   - Nepali responses when requested
   - Vision identifies landmark/food/text from image URL (Gemini Vision)
4. Iterate until all tests pass reliably.

**Phase 1 user stories (POC)**
1. As a traveler, I ask “Plan a 2-day budget trip in Pokhara under NPR 5000” and get a structured, reasoned plan.
2. As a user, I ask “What’s the weather in Kathmandu and what should I do today?” and get weather + activities.
3. As a tourist, I ask in Nepali for cultural etiquette and get accurate Nepali guidance.
4. As a user, I upload a temple photo URL and the Vision agent identifies it and explains context.
5. As a user, I ask for monsoon/landslide safety advice for a route and get safety-first guidance.

---

### Phase 2 — V1 App Development (Core App around proven CityBrain; **no auth yet**) 
**Goal:** working MVP with premium UX and stable backend APIs.

**Backend (FastAPI + MongoDB)**
1. Clean architecture + feature-based modules:
   - `chat` (CityBrain endpoint; conversation persistence)
   - `places` (hotels/restaurants/attractions/events; geo search; details)
   - `trips` (itineraries from CityBrain; saved trips CRUD)
   - `budget` (budget plans CRUD)
   - `weather` (Open-Meteo proxy)
   - `emergency` (Nepal numbers + nearest hospitals/police via geo)
   - `reviews`, `favorites`, `profile` (basic CRUD; unauth “demo user”)
2. MongoDB: 2dsphere indexes for places + emergency POIs.
3. Curated Nepal seed dataset (real places) + import script.
4. Validation + error handling + rate limiting + audit logs (basic).

**Frontend (React + Tailwind + shadcn/ui + Framer Motion + react-leaflet)**
1. App shell: responsive layout, light/dark, AA accessibility.
2. Screens:
   - Home/Landing
   - CityBrain Chat
   - Explore (Map + List + filters)
   - Place Detail (info, map pin, hours, reviews)
   - Trip Planner (generate + save)
   - Weather
   - Budget
   - Emergency Mode
   - Profile (demo)
3. Map: markers, filter chips, “near me”, selected place sync with list.

**Conclude Phase 2:** run `testing_agent_v3` (backend + frontend), fix all issues.

**Phase 2 user stories (V1)**
1. As a user, I can chat with CityBrain and get structured recommendations.
2. As a user, I can explore places on a map, filter by type, and see nearby results.
3. As a user, I can open a place detail page and read key info + reviews.
4. As a user, I can generate a day itinerary and save it.
5. As a user, I can open Emergency Mode and quickly see Nepal emergency numbers + nearest help.

---

### Phase 3 — Add Auth + Advanced Intelligence
**Goal:** add real user accounts + high-value intelligence features.

**Steps**
1. Auth:
   - Email/password (JWT) + Google OAuth
   - RBAC roles: user, business, admin
   - Migrate demo data → per-user collections
2. Camera AI UI (Vision): upload/capture → identify landmark/food/translate signboard.
3. Multilingual UI toggle (EN/NE) + translate agent.
4. Voice assistant (Web Speech input + TTS output).
5. Events + festival calendar; smarter routing (multi-stop optimization via CityBrain).
6. PWA Offline Mode: cache core screens + seed data.

**Conclude Phase 3:** run `testing_agent_v3`, fix all issues.

**Phase 3 user stories**
1. As a user, I can sign up/login (email + Google) and keep my saved trips/favorites.
2. As a user, I can take/upload a photo of a landmark and get identification + tips.
3. As a user, I can switch the app to Nepali UI and get Nepali AI responses.
4. As a user, I can speak a query and receive a spoken response.
5. As a traveler, I can build a multi-stop route and get an optimized plan.

---

### Phase 4 — Dashboards, Hardening, Release Readiness
**Goal:** admin/business tooling + production hardening.

**Steps**
1. Admin dashboard: manage places, reviews, users; seed data editor.
2. Business dashboard: claim listing, edit info, respond to reviews.
3. Security hardening: OWASP checks, stricter rate limiting, audit trails, backup strategy.
4. Observability: structured logs, health checks.
5. Final perf/accessibility pass; docs (README, API docs, deployment guide).

**Conclude Phase 4:** run `testing_agent_v3`, fix all issues.

**Phase 4 user stories**
1. As an admin, I can add/edit/remove places and see them on the map instantly.
2. As a business owner, I can claim my listing and update hours/photos.
3. As an admin, I can moderate reviews.
4. As a user, the app remains fast and accessible on mobile.
5. As an operator, I can deploy via Docker and verify health checks.

---

## 3) Next Actions (Immediate)
1. Do websearch + integration playbook for Emergent Google models (Gemma vs Gemini) + Vision.
2. Implement `test_core.py` + minimal CityBrain modules; run until all Phase 1 stories pass.
3. Confirm model selection outcome (Gemma if available; otherwise Gemini fallback) and lock prompts/schema.

---

## 4) Success Criteria
- Phase 1: `test_core.py` passes all scenarios with strict structured JSON, real weather, Nepali output, and working vision.
- Phase 2: V1 app supports chat + map exploration + details + trip/budget/emergency flows with stable APIs.
- Phase 3: Auth (email+Google) works; vision/voice/multilingual/offline features function end-to-end.
- Phase 4: Admin/business dashboards functional; security/perf/accessibility validated; deployment documented.
