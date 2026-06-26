"""Places: hotels, restaurants, attractions, events (geo + filters)."""
from typing import Optional
from fastapi import APIRouter, Query, HTTPException

from ..core.db import db
from ..repositories import place_review_stats

router = APIRouter(prefix="/places", tags=["places"])


@router.get("/cities")
async def list_cities():
    pipeline = [{"$group": {"_id": "$city", "count": {"$sum": 1},
                            "region": {"$first": "$region"}}},
                {"$sort": {"count": -1}}]
    rows = await db.places.aggregate(pipeline).to_list(100)
    return [{"city": r["_id"], "region": r.get("region"), "count": r["count"]} for r in rows]


@router.get("")
async def list_places(
    type: Optional[str] = None,
    city: Optional[str] = None,
    q: Optional[str] = None,
    tag: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius_km: float = 50,
    sort: str = "rating",
    limit: int = Query(60, le=200),
    skip: int = 0,
):
    query = {}
    if type:
        query["type"] = type
    if city:
        query["city"] = city
    if tag:
        query["tags"] = tag
    if q:
        query["$or"] = [
            {"name": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"tags": {"$regex": q, "$options": "i"}},
            {"city": {"$regex": q, "$options": "i"}},
        ]

    if lat is not None and lon is not None:
        query["location"] = {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                "$maxDistance": radius_km * 1000,
            }
        }
        cursor = db.places.find(query, {"_id": 0}).limit(limit)
    else:
        sort_field = {"rating": ("rating", -1), "price_low": ("price_npr", 1),
                      "price_high": ("price_npr", -1), "name": ("name", 1)}.get(sort, ("rating", -1))
        cursor = db.places.find(query, {"_id": 0}).sort([sort_field]).skip(skip).limit(limit)

    return await cursor.to_list(limit)


@router.get("/{place_id}")
async def get_place(place_id: str):
    place = await db.places.find_one({"id": place_id}, {"_id": 0})
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    stats = await place_review_stats(place_id)
    place.update(stats)
    # nearby places (same city, exclude self)
    nearby = await db.places.find(
        {"city": place["city"], "id": {"$ne": place_id}}, {"_id": 0}
    ).sort("rating", -1).limit(6).to_list(6)
    place["nearby"] = nearby
    return place
