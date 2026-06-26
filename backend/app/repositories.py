"""Repository helpers shared across routers."""
from typing import List, Dict, Any, Optional

from .core.db import db


async def place_lookup(city: str, ptype: Optional[str] = None) -> List[Dict[str, Any]]:
    """Used by CityBrain agents to ground reasoning in the live catalog."""
    q: Dict[str, Any] = {}
    if city:
        q["city"] = city
    if ptype:
        q["type"] = ptype
    cur = db.places.find(q, {"_id": 0}).sort("rating", -1).limit(20)
    return await cur.to_list(20)


async def place_review_stats(place_id: str) -> Dict[str, Any]:
    pipeline = [
        {"$match": {"place_id": place_id}},
        {"$group": {"_id": "$place_id", "avg": {"$avg": "$rating"}, "count": {"$sum": 1}}},
    ]
    rows = await db.reviews.aggregate(pipeline).to_list(1)
    if rows:
        return {"review_avg": round(rows[0]["avg"], 1), "review_count": rows[0]["count"]}
    return {"review_avg": None, "review_count": 0}
