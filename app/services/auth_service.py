from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories import user_repo
from app.schemas.auth import LoginIn, RegisterIn, TokenOut
from app.schemas.user import UserOut


async def register(db: AsyncSession, data: RegisterIn) -> TokenOut:
    if await user_repo.get_by_email(db, data.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email já registrado")
    if await user_repo.get_by_nickname(db, data.nickname):
        raise HTTPException(status.HTTP_409_CONFLICT, "Nickname já em uso")

    user = await user_repo.create(
        db,
        email=data.email,
        nickname=data.nickname,
        password_hash=hash_password(data.password),
    )
    return _token_for(user)


async def login(db: AsyncSession, data: LoginIn) -> TokenOut:
    user = await user_repo.get_by_identifier(db, data.identifier)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciais inválidas")
    return _token_for(user)


def _token_for(user: User) -> TokenOut:
    token = create_access_token(str(user.id))
    return TokenOut(access_token=token, user=UserOut.model_validate(user))
