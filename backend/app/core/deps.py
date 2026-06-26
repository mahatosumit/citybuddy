"""Shared dependencies. Phase 2 uses a fixed demo user so all flows are
testable without auth; Phase 3 swaps this for real JWT/Google auth."""
from fastapi import Header
from typing import Optional

DEMO_USER_ID = "demo-user"


async def current_user_id(x_user_id: Optional[str] = Header(default=None)) -> str:
    """Return the active user id. Falls back to the demo user in Phase 2."""
    return x_user_id or DEMO_USER_ID
