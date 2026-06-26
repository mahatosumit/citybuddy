"""User profile (demo user in Phase 2)."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends

from ..core.db import db
from ..core.deps import current_user_id
from ..schemas import ProfileUpdate

router = APIRouter(prefix="/profile", tags=["profile"])

_DEFAULT = {"name": "Demo Traveler", "home_city": "Kathmandu", "language": "en",
            "preferences": {"interests": ["culture", "nature", "food"], "budget_level": "mid"}}


@router.get("")
async def get_profile(user_id: str = Depends(current_user_id)):
    prof = await db.profiles.find_one({"user_id": user_id}, {"_id": 0})
    if not prof:
        prof = {"user_id": user_id, **_DEFAULT,
                "created_at": datetime.now(timezone.utc).isoformat()}
        await db.profiles.insert_one(dict(prof))
        prof.pop("_id", None)
    return prof


@router.put("")
async def update_profile(req: ProfileUpdate, user_id: str = Depends(current_user_id)):
    update = {k: v for k, v in req.model_dump().items() if v is not None}
    update["updated_at"] = datetime.now(timezone.utc).isoformat()
    await db.profiles.update_one({"user_id": user_id}, {"$set": {"user_id": user_id, **update}}, upsert=True)
    return await db.profiles.find_one({"user_id": user_id}, {"_id": 0})
