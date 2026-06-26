"""Admin dashboard endpoints (role=admin)."""
import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..core.db import db
from ..core.auth import require_role, serialize_doc

router = APIRouter(prefix="/admin", tags=["admin"])
admin_only = require_role("admin")


class PlaceUpsert(BaseModel):
    name: str
    type: str = "attraction"
    city: str = "Kathmandu"
    region: str = "Bagmati"
    lat: float = 27.7172
    lon: float = 85.324
    price_npr: float = 0
    rating: float = 4.5
    tags: list = []
    hours: str = ""
    description: str = ""
    image_url: str = ""


class RoleUpdate(BaseModel):
    role: str


@router.get("/stats")
async def stats(admin=Depends(admin_only)):
    return {
        "users": await db.users.count_documents({}),
        "places": await db.places.count_documents({}),
        "reviews": await db.reviews.count_documents({}),
        "trips": await db.trips.count_documents({}),
        "businesses": await db.users.count_documents({"role": "business"}),
        "conversations": await db.conversations.count_documents({}),
        "by_type": {r["_id"]: r["count"] async for r in db.places.aggregate(
            [{"$group": {"_id": "$type", "count": {"$sum": 1}}}])},
    }


@router.get("/users")
async def list_users(admin=Depends(admin_only)):
    users = await db.users.find({}, {"_id": 0, "password_hash": 0}).sort("created_at", -1).to_list(500)
    return [serialize_doc(u) for u in users]


@router.put("/users/{user_id}/role")
async def set_role(user_id: str, req: RoleUpdate, admin=Depends(admin_only)):
    if req.role not in ("user", "business", "admin"):
        raise HTTPException(status_code=400, detail="Invalid role")
    await db.users.update_one({"user_id": user_id}, {"$set": {"role": req.role}})
    return {"ok": True}


@router.post("/places")
async def create_place(req: PlaceUpsert, admin=Depends(admin_only)):
    slug = req.name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace("&", "and")
    doc = req.model_dump()
    doc.update({"id": slug, "location": {"type": "Point", "coordinates": [req.lon, req.lat]},
                "address": f"{req.city}, {req.region}, Nepal"})
    if not doc.get("image_url"):
        doc["image_url"] = "https://images.pexels.com/photos/19279803/pexels-photo-19279803.jpeg?auto=compress&cs=tinysrgb&w=1200"
    await db.places.update_one({"id": slug}, {"$set": doc}, upsert=True)
    return await db.places.find_one({"id": slug}, {"_id": 0})


@router.put("/places/{place_id}")
async def update_place(place_id: str, req: PlaceUpsert, admin=Depends(admin_only)):
    existing = await db.places.find_one({"id": place_id}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Place not found")
    doc = req.model_dump()
    doc["location"] = {"type": "Point", "coordinates": [req.lon, req.lat]}
    if not doc.get("image_url"):
        doc["image_url"] = existing.get("image_url")
    await db.places.update_one({"id": place_id}, {"$set": doc})
    return await db.places.find_one({"id": place_id}, {"_id": 0})


@router.delete("/places/{place_id}")
async def delete_place(place_id: str, admin=Depends(admin_only)):
    await db.places.delete_one({"id": place_id})
    return {"ok": True}


@router.get("/reviews")
async def all_reviews(admin=Depends(admin_only)):
    return await db.reviews.find({}, {"_id": 0}).sort("created_at", -1).limit(200).to_list(200)


@router.delete("/reviews/{review_id}")
async def delete_review(review_id: str, admin=Depends(admin_only)):
    await db.reviews.delete_one({"id": review_id})
    return {"ok": True}
