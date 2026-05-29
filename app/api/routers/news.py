from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.news import NewsSearchIn, NewsSearchOut
from app.services import news_service

router = APIRouter(prefix="/news", tags=["news"])


@router.post("/search", response_model=NewsSearchOut)
async def search(
    data: NewsSearchIn,
    _user: User = Depends(get_current_user),
) -> NewsSearchOut:
    return await news_service.search(data)
