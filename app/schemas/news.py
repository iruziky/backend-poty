from typing import Any

from pydantic import BaseModel, Field


class NewsIn(BaseModel):
    id: int
    title: str
    summary: str | None = ""
    model_config = {"extra": "allow"}


class NewsSearchIn(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    items: list[NewsIn]
    limit: int = Field(default=20, ge=1, le=100)


class NewsSearchOut(BaseModel):
    results: list[dict[str, Any]]
