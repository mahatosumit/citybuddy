"""Camera AI / Vision endpoint (Gemini multimodal)."""
from fastapi import APIRouter, HTTPException

from ..schemas import VisionRequest
from ..citybrain import orchestrator

router = APIRouter(prefix="/vision", tags=["vision"])


@router.post("/analyze")
async def analyze(req: VisionRequest):
    if not req.image_base64:
        raise HTTPException(status_code=400, detail="image_base64 required")
    # strip data URL prefix if present
    b64 = req.image_base64
    if "," in b64 and b64.strip().startswith("data:"):
        b64 = b64.split(",", 1)[1]
    try:
        result = await orchestrator.analyze_image(b64, note=req.note or "")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Vision error: {e}")
    return result
