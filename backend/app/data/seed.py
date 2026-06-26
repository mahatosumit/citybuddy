"""Idempotent database seeding for the curated Nepal dataset."""
import logging

from ..core.db import db
from .seed_data import build_places, build_emergency_pois

logger = logging.getLogger("citybuddy.seed")


async def seed_if_needed(force: bool = False) -> dict:
    result = {"places": 0, "emergency_pois": 0, "skipped": False}

    places_count = await db.places.count_documents({})
    if force or places_count == 0:
        places = build_places()
        # upsert by id to stay idempotent
        for p in places:
            await db.places.update_one({"id": p["id"]}, {"$set": p}, upsert=True)
        result["places"] = len(places)
        logger.info("Seeded %d places", len(places))
    else:
        result["skipped"] = True

    epoi_count = await db.emergency_pois.count_documents({})
    if force or epoi_count == 0:
        pois = build_emergency_pois()
        for p in pois:
            await db.emergency_pois.update_one({"id": p["id"]}, {"$set": p}, upsert=True)
        result["emergency_pois"] = len(pois)
        logger.info("Seeded %d emergency POIs", len(pois))

    return result
