import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr
    nickname: str
    has_played_today: bool
    daily_score: int
    streak_days: int
    last_played_date: date | None
