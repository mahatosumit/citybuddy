"""CityBuddy API - FastAPI application entrypoint."""
import logging

from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from app.core.db import ensure_indexes, client
from app.data.seed import seed_if_needed
from app.routers import (
    auth, chat, places, reviews, favorites, trips, budget, weather, emergency, nepal, vision, profile,
    admin, business,
)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("citybuddy")

app = FastAPI(title="CityBuddy API", version="1.0.0",
              description="AI city companion for Nepal - powered by CityBrain")

api_router = APIRouter(prefix="/api")


@api_router.get("/")
async def root():
    return {"message": "CityBuddy API", "status": "ok", "product": "Your AI Companion for Nepal"}


@api_router.get("/health")
async def health():
    return {"status": "healthy"}


# Mount feature routers under /api
for r in (auth, chat, places, reviews, favorites, trips, budget, weather, emergency, nepal, vision, profile, admin, business):
    api_router.include_router(r.router)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    try:
        await ensure_indexes()
        res = await seed_if_needed()
        logger.info("Startup seed: %s", res)
    except Exception as e:
        logger.exception("Startup initialization failed: %s", e)


@app.on_event("shutdown")
async def on_shutdown():
    client.close()
