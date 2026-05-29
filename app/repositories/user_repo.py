import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def get_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    return await db.get(User, user_id)


async def get_by_email(db: AsyncSession, email: str) -> User | None:
    res = await db.execute(select(User).where(User.email == email.lower()))
    return res.scalar_one_or_none()


async def get_by_nickname(db: AsyncSession, nickname: str) -> User | None:
    res = await db.execute(select(User).where(User.nickname == nickname))
    return res.scalar_one_or_none()


async def get_by_identifier(db: AsyncSession, identifier: str) -> User | None:
    if "@" in identifier:
        return await get_by_email(db, identifier)
    return await get_by_nickname(db, identifier)


async def create(db: AsyncSession, *, email: str, nickname: str, password_hash: str) -> User:
    user = User(email=email.lower(), nickname=nickname, password_hash=password_hash)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
