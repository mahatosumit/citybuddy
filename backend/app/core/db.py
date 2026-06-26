"""MongoDB connection + helpers (single shared async client)."""
import os
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

ROOT_DIR = Path(__file__).resolve().parents[2]  # /app/backend
load_dotenv(ROOT_DIR / ".env")

_mongo_url = os.environ["MONGO_URL"]
_db_name = os.environ.get("DB_NAME", "citybuddy")

client = AsyncIOMotorClient(_mongo_url)
db: AsyncIOMotorDatabase = client[_db_name]


def get_db() -> AsyncIOMotorDatabase:
    return db


async def ensure_indexes() -> None:
    """Create geospatial + lookup indexes (idempotent)."""
    await db.places.create_index([("location", "2dsphere")])
    await db.places.create_index("id", unique=True)
    await db.places.create_index("type")
    await db.places.create_index("city")
    await db.emergency_pois.create_index([("location", "2dsphere")])
    await db.emergency_pois.create_index("id", unique=True)
    await db.conversations.create_index("id", unique=True)
    await db.conversations.create_index("user_id")
    await db.messages.create_index("conversation_id")
    await db.trips.create_index("id", unique=True)
    await db.trips.create_index("user_id")
    await db.budgets.create_index("id", unique=True)
    await db.budgets.create_index("user_id")
    await db.reviews.create_index("place_id")
    await db.favorites.create_index([("user_id", 1), ("place_id", 1)], unique=True)
    await db.profiles.create_index("user_id", unique=True)
    # auth
    await db.users.create_index("user_id", unique=True)
    await db.users.create_index("email", unique=True)
    await db.user_sessions.create_index("session_token", unique=True)
    await db.user_sessions.create_index("user_id")
