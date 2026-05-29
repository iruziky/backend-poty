from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.discover import RecommendIn, RecommendOut
from app.services import discover_service

router = APIRouter(prefix="/discover", tags=["discover"])


@router.post("/recommend", response_model=RecommendOut)
async def recommend(
    data: RecommendIn,
    _user: User = Depends(get_current_user),
) -> RecommendOut:
    return await discover_service.recommend(data)
