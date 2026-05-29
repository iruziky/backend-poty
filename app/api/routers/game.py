from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.db import get_db
from app.models.user import User
from app.schemas.game import PercentileOut, RankingOut, SubmitIn
from app.schemas.user import UserOut
from app.services import game_service

router = APIRouter(prefix="/game", tags=["game"])


@router.post("/submit", response_model=UserOut)
async def submit(
    data: SubmitIn,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserOut:
    return await game_service.submit(db, user, data)


@router.get("/percentile", response_model=PercentileOut)
async def percentile(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> PercentileOut:
    return await game_service.percentile(db, user)


@router.get("/ranking", response_model=RankingOut)
async def ranking(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> RankingOut:
    return await game_service.ranking(db, user)
