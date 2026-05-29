from datetime import date, timedelta

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories import game_repo
from app.schemas.game import (
    MeRanking,
    PercentileOut,
    RankingEntry,
    RankingOut,
    SubmitIn,
)
from app.schemas.user import UserOut


def apply_daily_reset(user: User) -> User:
    """Reflete estado 'zerado' quando o último jogo não foi hoje.
    Não persiste no DB — só ajusta a instância retornada."""
    today = date.today()
    if user.last_played_date != today:
        user.has_played_today = False
        user.daily_score = 0
    return user


def user_out(user: User) -> UserOut:
    return UserOut.model_validate(apply_daily_reset(user))


async def submit(db: AsyncSession, user: User, data: SubmitIn) -> UserOut:
    today = date.today()
    if user.last_played_date == today:
        raise HTTPException(status.HTTP_409_CONFLICT, "Você já jogou hoje")

    if user.last_played_date == today - timedelta(days=1):
        user.streak_days += 1
    else:
        user.streak_days = 1

    user.daily_score = data.score
    user.has_played_today = True
    user.last_played_date = today

    await db.commit()
    await db.refresh(user)
    return UserOut.model_validate(user)


async def percentile(db: AsyncSession, user: User) -> PercentileOut:
    today = date.today()
    if user.last_played_date != today:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Jogue hoje para ver seu percentil")

    total = await game_repo.count_today(db, today)
    if total <= 1:
        return PercentileOut(percentile=100, total_players_today=total)

    worse = await game_repo.count_worse_today(db, today, user.daily_score)
    pct = round(100 * worse / max(total - 1, 1))
    return PercentileOut(percentile=pct, total_players_today=total)


async def ranking(db: AsyncSession, user: User) -> RankingOut:
    today = date.today()
    top_users = await game_repo.top_n_today(db, today, n=10)
    top_entries = [
        RankingEntry(rank=i + 1, user_id=u.id, nickname=u.nickname, score=u.daily_score)
        for i, u in enumerate(top_users)
    ]

    played_today = user.last_played_date == today
    score = user.daily_score if played_today else 0
    in_top = any(e.user_id == user.id for e in top_entries)
    me_rank = await game_repo.rank_today(db, today, score) if played_today else None

    return RankingOut(
        top=top_entries,
        me=MeRanking(
            rank=me_rank,
            user_id=user.id,
            nickname=user.nickname,
            score=score,
            in_top=in_top,
        ),
    )
