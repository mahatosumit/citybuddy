"""User profile = the authenticated user's editable fields."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends

from ..core.db import db
from ..core.auth import get_current_user, serialize_doc
from ..schemas import ProfileUpdate

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("")
async def get_profile(user=Depends(get_current_user)):
    return serialize_doc(user)


@router.put("")
async def update_profile(req: ProfileUpdate, user=Depends(get_current_user)):
    update = {k: v for k, v in req.model_dump().items() if v is not None}
    update["updated_at"] = datetime.now(timezone.utc).isoformat()
    await db.users.update_one({"user_id": user["user_id"]}, {"$set": update})
    updated = await db.users.find_one({"user_id": user["user_id"]}, {"_id": 0})
    return serialize_doc(updated)
