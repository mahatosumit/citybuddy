"""Authentication core: password hashing, JWT, Emergent Google session,
unified user resolution, RBAC dependencies, and Mongo serialization helper.

Supports TWO auth methods that coexist in one `users` collection:
  1. Email/password  -> we issue a JWT (Bearer)
  2. Google (Emergent-managed) -> session_token stored in `user_sessions`
The `get_current_user` dependency accepts either a cookie `session_token`
or an `Authorization: Bearer <token>` header.
"""
import os
import uuid
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

import jwt
import bcrypt
from dotenv import load_dotenv
from fastapi import Request, HTTPException, Depends

from .db import db

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

logger = logging.getLogger("citybuddy.auth")

JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret-change-me")
JWT_ALGO = "HS256"
JWT_DAYS = 7
SESSION_DAYS = 7
EMERGENT_SESSION_URL = "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data"


# ----------------------------- helpers -----------------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def create_jwt(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=JWT_DAYS),
        "kind": "email",
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def decode_jwt(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload.get("sub")
    except Exception:
        return None


def serialize_doc(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Strip Mongo _id, password_hash, and convert datetimes to ISO strings."""
    if not doc:
        return doc
    out = {}
    for k, v in doc.items():
        if k in ("_id", "password_hash"):
            continue
        out[k] = v.isoformat() if isinstance(v, datetime) else v
    return out


def _now():
    return datetime.now(timezone.utc)


# ----------------------------- user creation -----------------------------
async def get_or_create_oauth_user(email: str, name: str, picture: str = "") -> Dict[str, Any]:
    existing = await db.users.find_one({"email": email}, {"_id": 0})
    if existing:
        # keep profile picture/name fresh
        await db.users.update_one({"user_id": existing["user_id"]},
                                  {"$set": {"name": name or existing.get("name"),
                                            "picture": picture or existing.get("picture")}})
        return existing
    return await _create_user(email=email, name=name, picture=picture, provider="google")


async def _create_user(email: str, name: str, password_hash: str = None,
                       picture: str = "", provider: str = "email") -> Dict[str, Any]:
    is_first = (await db.users.count_documents({})) == 0
    user = {
        "user_id": f"user_{uuid.uuid4().hex[:12]}",
        "email": email.lower().strip(),
        "name": name or email.split("@")[0],
        "picture": picture,
        "role": "admin" if is_first else "user",
        "auth_provider": provider,
        "home_city": "Kathmandu",
        "language": "en",
        "preferences": {"interests": ["culture", "nature", "food"], "budget_level": "mid"},
        "created_at": _now(),
    }
    if password_hash:
        user["password_hash"] = password_hash
    await db.users.insert_one(user)
    logger.info("Created user %s (%s) role=%s", user["email"], provider, user["role"])
    return user


async def create_session(user_id: str, session_token: str = None) -> str:
    token = session_token or f"sess_{uuid.uuid4().hex}"
    await db.user_sessions.insert_one({
        "user_id": user_id,
        "session_token": token,
        "expires_at": _now() + timedelta(days=SESSION_DAYS),
        "created_at": _now(),
    })
    return token


# ----------------------------- resolution -----------------------------
def _extract_token(request: Request) -> Optional[str]:
    token = request.cookies.get("session_token")
    if token:
        return token
    auth = request.headers.get("Authorization") or request.headers.get("authorization")
    if auth and auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1].strip()
    return None


async def _user_from_token(token: str) -> Optional[Dict[str, Any]]:
    if not token:
        return None
    # 1) Try DB session (Google / Emergent)
    sess = await db.user_sessions.find_one({"session_token": token}, {"_id": 0})
    if sess:
        expires_at = sess.get("expires_at")
        if isinstance(expires_at, str):
            expires_at = datetime.fromisoformat(expires_at)
        if expires_at and expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at and expires_at < _now():
            return None
        return await db.users.find_one({"user_id": sess["user_id"]}, {"_id": 0})
    # 2) Try JWT (email/password)
    uid = decode_jwt(token)
    if uid:
        return await db.users.find_one({"user_id": uid}, {"_id": 0})
    return None


async def get_optional_user(request: Request) -> Optional[Dict[str, Any]]:
    return await _user_from_token(_extract_token(request))


async def get_current_user(request: Request) -> Dict[str, Any]:
    user = await _user_from_token(_extract_token(request))
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


def require_role(*roles: str):
    async def _checker(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        if user.get("role") not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return _checker
