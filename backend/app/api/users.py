from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import User as UserSchema
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/me", response_model=UserSchema)
async def read_users_me(
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    return current_user