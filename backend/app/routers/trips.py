"""Trip planner: public AI generation + per-user saved trips."""
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException

from ..core.db import db
from ..core.auth import get_current_user
from ..schemas import TripGenerateRequest, TripSaveRequest
from ..citybrain import orchestrator
from ..repositories import place_lookup

router = APIRouter(prefix="/trips", tags=["trips"])


def _now():
    return datetime.now(timezone.utc).isoformat()


@router.post("/generate")
async def generate_trip(req: TripGenerateRequest):
    try:
        plan = await orchestrator.plan_trip(
            city=req.city, days=max(1, min(req.days, 10)), budget_npr=req.budget_npr,
            interests=req.interests, language=req.language, place_lookup=place_lookup)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Trip planner error: {e}")
    return plan


@router.get("")
async def list_trips(user=Depends(get_current_user)):
    return await db.trips.find({"user_id": user["user_id"]}, {"_id": 0}).sort("created_at", -1).to_list(200)


@router.post("")
async def save_trip(req: TripSaveRequest, user=Depends(get_current_user)):
    trip = req.model_dump()
    trip.update({"id": str(uuid.uuid4()), "user_id": user["user_id"], "created_at": _now()})
    await db.trips.insert_one(dict(trip))
    trip.pop("_id", None)
    return trip


@router.get("/{trip_id}")
async def get_trip(trip_id: str, user=Depends(get_current_user)):
    trip = await db.trips.find_one({"id": trip_id, "user_id": user["user_id"]}, {"_id": 0})
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.delete("/{trip_id}")
async def delete_trip(trip_id: str, user=Depends(get_current_user)):
    await db.trips.delete_one({"id": trip_id, "user_id": user["user_id"]})
    return {"ok": True}
