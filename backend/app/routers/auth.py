"""Authentication routes: email/password + Emergent Google session."""
import logging
from datetime import datetime, timezone

import httpx
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from pydantic import BaseModel, EmailStr, Field

from ..core.db import db
from ..core.auth import (
    hash_password, verify_password, create_jwt, _create_user, create_session,
    get_or_create_oauth_user, get_current_user, serialize_doc, EMERGENT_SESSION_URL,
)

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger("citybuddy.auth")

COOKIE_KW = dict(httponly=True, secure=True, samesite="none", path="/", max_age=7 * 24 * 3600)


class RegisterReq(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str = ""


class LoginReq(BaseModel):
    email: EmailStr
    password: str


class GoogleSessionReq(BaseModel):
    session_id: str


@router.post("/register")
async def register(req: RegisterReq, response: Response):
    existing = await db.users.find_one({"email": req.email.lower().strip()}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = await _create_user(email=req.email, name=req.name,
                              password_hash=hash_password(req.password), provider="email")
    token = create_jwt(user["user_id"])
    response.set_cookie("session_token", token, **COOKIE_KW)
    return {"token": token, "user": serialize_doc(user)}


@router.post("/login")
async def login(req: LoginReq, response: Response):
    user = await db.users.find_one({"email": req.email.lower().strip()})
    if not user or not user.get("password_hash") or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_jwt(user["user_id"])
    response.set_cookie("session_token", token, **COOKIE_KW)
    return {"token": token, "user": serialize_doc(user)}


@router.post("/google/session")
async def google_session(req: GoogleSessionReq, response: Response):
    """Exchange an Emergent session_id for user data + persistent session_token."""
    try:
        async with httpx.AsyncClient(timeout=20) as cx:
            r = await cx.get(EMERGENT_SESSION_URL, headers={"X-Session-ID": req.session_id})
            r.raise_for_status()
            data = r.json()
    except Exception as e:
        logger.exception("Emergent session exchange failed")
        raise HTTPException(status_code=401, detail=f"Google session invalid: {e}")

    email = data.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="No email from Google session")
    user = await get_or_create_oauth_user(email=email, name=data.get("name", ""),
                                          picture=data.get("picture", ""))
    token = await create_session(user["user_id"], session_token=data.get("session_token"))
    response.set_cookie("session_token", token, **COOKIE_KW)
    return {"token": token, "user": serialize_doc(user)}


@router.get("/me")
async def me(user=Depends(get_current_user)):
    return serialize_doc(user)


@router.post("/logout")
async def logout(request: Request, response: Response):
    token = request.cookies.get("session_token")
    if not token:
        auth = request.headers.get("Authorization", "")
        if auth.lower().startswith("bearer "):
            token = auth.split(" ", 1)[1]
    if token:
        await db.user_sessions.delete_one({"session_token": token})
    response.delete_cookie("session_token", path="/")
    return {"ok": True}


@router.post("/register-business")
async def register_business(user=Depends(get_current_user)):
    """Upgrade the current user to a business account."""
    if user.get("role") == "admin":
        raise HTTPException(status_code=400, detail="Admins cannot be downgraded to business")
    await db.users.update_one({"user_id": user["user_id"]}, {"$set": {"role": "business"}})
    updated = await db.users.find_one({"user_id": user["user_id"]}, {"_id": 0})
    return serialize_doc(updated)
