"""CityBrain chat endpoints. Anonymous users get full AI answers; logged-in
users also get persisted conversation history."""
import uuid
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from ..core.db import db
from ..core.auth import get_optional_user, get_current_user
from ..schemas import ChatRequest
from ..citybrain import orchestrator
from ..repositories import place_lookup

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger("citybuddy.chat")


def _now():
    return datetime.now(timezone.utc).isoformat()


@router.post("/message")
async def send_message(req: ChatRequest, user=Depends(get_optional_user)):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        result = await orchestrator.process(req.message, context=req.context or {},
                                            place_lookup=place_lookup)
    except Exception as e:
        logger.exception("CityBrain failed")
        raise HTTPException(status_code=502, detail=f"CityBrain error: {e}")

    conv_id = None
    assistant_msg = {"id": str(uuid.uuid4()), "role": "assistant",
                     "content": result.get("summary", ""), "data": result, "created_at": _now()}

    # Persist only for authenticated users
    if user:
        uid = user["user_id"]
        conv_id = req.conversation_id
        if conv_id:
            conv = await db.conversations.find_one({"id": conv_id, "user_id": uid}, {"_id": 0})
            if not conv:
                conv_id = None
        if not conv_id:
            conv_id = str(uuid.uuid4())
            title = req.message.strip()[:48] + ("\u2026" if len(req.message.strip()) > 48 else "")
            await db.conversations.insert_one({"id": conv_id, "user_id": uid, "title": title,
                                               "created_at": _now(), "updated_at": _now()})
        await db.messages.insert_one({"id": str(uuid.uuid4()), "conversation_id": conv_id,
                                      "role": "user", "content": req.message, "created_at": _now()})
        await db.messages.insert_one({**assistant_msg, "conversation_id": conv_id})
        await db.conversations.update_one({"id": conv_id}, {"$set": {"updated_at": _now()}})

    return {"conversation_id": conv_id, "message": assistant_msg, "response": result}


@router.get("/conversations")
async def list_conversations(user=Depends(get_current_user)):
    cur = db.conversations.find({"user_id": user["user_id"]}, {"_id": 0}).sort("updated_at", -1).limit(100)
    return await cur.to_list(100)


@router.get("/conversations/{conv_id}")
async def get_conversation(conv_id: str, user=Depends(get_current_user)):
    conv = await db.conversations.find_one({"id": conv_id, "user_id": user["user_id"]}, {"_id": 0})
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    msgs = await db.messages.find({"conversation_id": conv_id}, {"_id": 0}).sort("created_at", 1).to_list(500)
    return {"conversation": conv, "messages": msgs}


@router.delete("/conversations/{conv_id}")
async def delete_conversation(conv_id: str, user=Depends(get_current_user)):
    await db.conversations.delete_one({"id": conv_id, "user_id": user["user_id"]})
    await db.messages.delete_many({"conversation_id": conv_id})
    return {"ok": True}
