"""Pydantic request/response schemas."""
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class TripGenerateRequest(BaseModel):
    city: str = "Kathmandu"
    days: int = 2
    budget_npr: Optional[float] = None
    interests: Optional[List[str]] = None
    language: str = "en"


class TripSaveRequest(BaseModel):
    title: str
    city: str
    days: int
    summary: Optional[str] = ""
    estimated_cost_npr: Optional[float] = None
    itinerary: List[Dict[str, Any]] = Field(default_factory=list)
    tips: List[str] = Field(default_factory=list)
    safety_notes: List[str] = Field(default_factory=list)


class BudgetEntry(BaseModel):
    category: str
    label: str
    amount_npr: float


class BudgetCreate(BaseModel):
    title: str
    city: Optional[str] = ""
    total_budget_npr: float = 0
    entries: List[BudgetEntry] = Field(default_factory=list)


class ReviewCreate(BaseModel):
    rating: float = Field(ge=1, le=5)
    comment: str = ""
    user_name: str = "Traveler"


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    home_city: Optional[str] = None
    language: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class VisionRequest(BaseModel):
    image_base64: str
    note: Optional[str] = ""
