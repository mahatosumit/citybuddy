"""Business dashboard endpoints (role=business or admin)."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from ..core.db import db
from ..core.auth import require_role

router = APIRouter(prefix="/business", tags=["business"])
biz_only = require_role("business", "admin")


class ClaimReq(BaseModel):
    place_id: str


class BusinessPlaceUpdate(BaseModel):
    description: Optional[str] = None
    hours: Optional[str] = None
    price_npr: Optional[float] = None
    image_url: Optional[str] = None


class ReplyReq(BaseModel):
    reply: str


@router.post("/claim")
async def claim_place(req: ClaimReq, user=Depends(biz_only)):
    place = await db.places.find_one({"id": req.place_id}, {"_id": 0})
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    if place.get("owner_id") and place["owner_id"] != user["user_id"]:
        raise HTTPException(status_code=409, detail="Already claimed by another business")
    await db.places.update_one({"id": req.place_id}, {"$set": {"owner_id": user["user_id"]}})
    return {"ok": True, "place_id": req.place_id}


@router.get("/listings")
async def my_listings(user=Depends(biz_only)):
    return await db.places.find({"owner_id": user["user_id"]}, {"_id": 0}).to_list(200)


@router.put("/listings/{place_id}")
async def update_listing(place_id: str, req: BusinessPlaceUpdate, user=Depends(biz_only)):
    place = await db.places.find_one({"id": place_id}, {"_id": 0})
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    if place.get("owner_id") != user["user_id"] and user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="You do not own this listing")
    update = {k: v for k, v in req.model_dump().items() if v is not None}
    if update:
        await db.places.update_one({"id": place_id}, {"$set": update})
    return await db.places.find_one({"id": place_id}, {"_id": 0})


@router.get("/reviews")
async def listing_reviews(user=Depends(biz_only)):
    listings = await db.places.find({"owner_id": user["user_id"]}, {"_id": 0, "id": 1, "name": 1}).to_list(200)
    ids = [l["id"] for l in listings]
    reviews = await db.reviews.find({"place_id": {"$in": ids}}, {"_id": 0}).sort("created_at", -1).to_list(300)
    return {"listings": listings, "reviews": reviews}


@router.post("/reviews/{review_id}/reply")
async def reply_review(review_id: str, req: ReplyReq, user=Depends(biz_only)):
    review = await db.reviews.find_one({"id": review_id}, {"_id": 0})
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    place = await db.places.find_one({"id": review["place_id"]}, {"_id": 0})
    if (not place or place.get("owner_id") != user["user_id"]) and user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not your listing")
    await db.reviews.update_one({"id": review_id},
                                {"$set": {"owner_reply": req.reply,
                                          "replied_at": datetime.now(timezone.utc).isoformat()}})
    return {"ok": True}
