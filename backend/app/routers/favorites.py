"""Favorites (saved places) per authenticated user."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException

from ..core.db import db
from ..core.auth import get_current_user

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("")
async def list_favorites(user=Depends(get_current_user)):
    favs = await db.favorites.find({"user_id": user["user_id"]}, {"_id": 0}).sort("created_at", -1).to_list(500)
    ids = [f["place_id"] for f in favs]
    places = await db.places.find({"id": {"$in": ids}}, {"_id": 0}).to_list(500)
    pmap = {p["id"]: p for p in places}
    return [pmap[i] for i in ids if i in pmap]


@router.get("/ids")
async def favorite_ids(user=Depends(get_current_user)):
    favs = await db.favorites.find({"user_id": user["user_id"]}, {"_id": 0, "place_id": 1}).to_list(1000)
    return [f["place_id"] for f in favs]


@router.post("/{place_id}")
async def add_favorite(place_id: str, user=Depends(get_current_user)):
    place = await db.places.find_one({"id": place_id}, {"_id": 0})
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    await db.favorites.update_one(
        {"user_id": user["user_id"], "place_id": place_id},
        {"$set": {"user_id": user["user_id"], "place_id": place_id,
                  "created_at": datetime.now(timezone.utc).isoformat()}}, upsert=True)
    return {"ok": True, "place_id": place_id, "favorited": True}


@router.delete("/{place_id}")
async def remove_favorite(place_id: str, user=Depends(get_current_user)):
    await db.favorites.delete_one({"user_id": user["user_id"], "place_id": place_id})
    return {"ok": True, "place_id": place_id, "favorited": False}
