"""Budget planner CRUD (per authenticated user)."""
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException

from ..core.db import db
from ..core.auth import get_current_user
from ..schemas import BudgetCreate

router = APIRouter(prefix="/budgets", tags=["budgets"])


def _now():
    return datetime.now(timezone.utc).isoformat()


@router.get("")
async def list_budgets(user=Depends(get_current_user)):
    return await db.budgets.find({"user_id": user["user_id"]}, {"_id": 0}).sort("created_at", -1).to_list(200)


@router.post("")
async def create_budget(req: BudgetCreate, user=Depends(get_current_user)):
    b = req.model_dump()
    b.update({"id": str(uuid.uuid4()), "user_id": user["user_id"], "created_at": _now(), "updated_at": _now()})
    await db.budgets.insert_one(dict(b))
    b.pop("_id", None)
    return b


@router.put("/{budget_id}")
async def update_budget(budget_id: str, req: BudgetCreate, user=Depends(get_current_user)):
    existing = await db.budgets.find_one({"id": budget_id, "user_id": user["user_id"]}, {"_id": 0})
    if not existing:
        raise HTTPException(status_code=404, detail="Budget not found")
    update = req.model_dump()
    update["updated_at"] = _now()
    await db.budgets.update_one({"id": budget_id}, {"$set": update})
    return await db.budgets.find_one({"id": budget_id}, {"_id": 0})


@router.delete("/{budget_id}")
async def delete_budget(budget_id: str, user=Depends(get_current_user)):
    await db.budgets.delete_one({"id": budget_id, "user_id": user["user_id"]})
    return {"ok": True}
