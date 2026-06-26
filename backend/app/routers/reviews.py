"""Reviews for places."""
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException

from ..core.db import db
from ..core.deps import current_user_id
from ..schemas import ReviewCreate

router = APIRouter(prefix="/places", tags=["reviews"])


@router.get("/{place_id}/reviews")
async def list_reviews(place_id: str):
    return await db.reviews.find({"place_id": place_id}, {"_id": 0}).sort("created_at", -1).to_list(200)


@router.post("/{place_id}/reviews")
async def add_review(place_id: str, req: ReviewCreate, user_id: str = Depends(current_user_id)):
    place = await db.places.find_one({"id": place_id}, {"_id": 0})
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    review = {
        "id": str(uuid.uuid4()), "place_id": place_id, "user_id": user_id,
        "user_name": req.user_name or "Traveler", "rating": req.rating,
        "comment": req.comment, "created_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.reviews.insert_one(dict(review))
    review.pop("_id", None)
    return review
