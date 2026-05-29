from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def top_n_today(db: AsyncSession, today: date, n: int = 10) -> list[User]:
    res = await db.execute(
        select(User)
        .where(User.last_played_date == today)
        .order_by(User.daily_score.desc(), User.created_at.asc())
        .limit(n)
    )
    return list(res.scalars().all())


async def count_today(db: AsyncSession, today: date) -> int:
    res = await db.execute(
        select(func.count()).select_from(User).where(User.last_played_date == today)
    )
    return int(res.scalar_one())


async def count_worse_today(db: AsyncSession, today: date, score: int) -> int:
    res = await db.execute(
        select(func.count())
        .select_from(User)
        .where(User.last_played_date == today, User.daily_score < score)
    )
    return int(res.scalar_one())


async def rank_today(db: AsyncSession, today: date, score: int) -> int:
    """1-based rank: número de usuários com score maior + 1."""
    res = await db.execute(
        select(func.count())
        .select_from(User)
        .where(User.last_played_date == today, User.daily_score > score)
    )
    return int(res.scalar_one()) + 1
