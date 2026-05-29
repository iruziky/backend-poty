import uuid

from pydantic import BaseModel, Field


class SubmitIn(BaseModel):
    score: int = Field(ge=0, le=10_000)


class PercentileOut(BaseModel):
    percentile: int
    total_players_today: int


class RankingEntry(BaseModel):
    rank: int
    user_id: uuid.UUID
    nickname: str
    score: int


class MeRanking(BaseModel):
    rank: int | None
    user_id: uuid.UUID
    nickname: str
    score: int
    in_top: bool


class RankingOut(BaseModel):
    top: list[RankingEntry]
    me: MeRanking
