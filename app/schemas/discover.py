from typing import Any

from pydantic import BaseModel, Field


class PlaceIn(BaseModel):
    id: int
    name: str
    location: str | None = None
    category: str | None = None
    description: str | None = None
    hours: str | None = None
    images: list[str] | None = None
    whatsapp: str | None = None
    instagram: str | None = None
    site: str | None = None
    # passa-thru de campos extras vindos do frontend
    model_config = {"extra": "allow"}


class RecommendIn(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    options: list[PlaceIn]
    limit: int = Field(default=5, ge=1, le=20)


class RecommendOut(BaseModel):
    recommendations: list[dict[str, Any]]
    source: str  # "llm" | "fallback"
