"""Emergency mode: numbers, nearest facilities, safety guidance."""
from typing import Optional
from fastapi import APIRouter, HTTPException

from ..core.db import db
from ..citybrain.nepal_knowledge import EMERGENCY_NUMBERS, SAFETY

router = APIRouter(prefix="/emergency", tags=["emergency"])


@router.get("/numbers")
async def numbers():
    return EMERGENCY_NUMBERS


@router.get("/nearby")
async def nearby(lat: float, lon: float, type: Optional[str] = None, limit: int = 10):
    query = {"location": {"$near": {"$geometry": {"type": "Point", "coordinates": [lon, lat]},
                                    "$maxDistance": 100000}}}
    if type:
        query["type"] = type
    rows = await db.emergency_pois.find(query, {"_id": 0}).limit(limit).to_list(limit)
    return rows


@router.get("/guidance")
async def guidance(type: str = "earthquake"):
    key = type.lower()
    if key not in SAFETY:
        raise HTTPException(status_code=404, detail="Unknown guidance type")
    return {"type": key, "steps": SAFETY[key]}


@router.get("/guidance-all")
async def guidance_all():
    return SAFETY
