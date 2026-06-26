"""Nepal Intelligence hub endpoints."""
from fastapi import APIRouter

from ..core.db import db
from ..citybrain import nepal_knowledge as nk

router = APIRouter(prefix="/nepal", tags=["nepal"])


@router.get("/overview")
async def overview():
    pipeline = [{"$group": {"_id": "$city", "count": {"$sum": 1}}}]
    rows = await db.places.aggregate(pipeline).to_list(100)
    counts = {r["_id"]: r["count"] for r in rows}
    cities = [{"city": k, **v, "place_count": counts.get(k, 0)} for k, v in nk.CITIES.items()]
    return {"cities": cities}


@router.get("/festivals")
async def festivals():
    return nk.FESTIVALS


@router.get("/treks")
async def treks():
    return nk.TREKS


@router.get("/unesco")
async def unesco():
    return nk.UNESCO_SITES


@router.get("/transport")
async def transport():
    return nk.TRANSPORT


@router.get("/info")
async def info():
    return {"practical": nk.PRACTICAL, "safety": nk.SAFETY, "etiquette": nk.ETIQUETTE}
