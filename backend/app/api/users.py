from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import User as UserSchema
from app.schemas.user import ErrorResponse
from fastapi import APIRouter, Depends, status

router = APIRouter()

NOT_FOUND_RESPONSE = {
    "model": ErrorResponse,
    "description": "The authenticated user could not be found.",
    "content": {
        "application/json": {
            "example": {"detail": "User not found"},
        }
    },
}

INTERNAL_SERVER_ERROR_RESPONSE = {
    "model": ErrorResponse,
    "description": "An unexpected server error occurred.",
    "content": {
        "application/json": {
            "example": {"detail": "Internal server error"},
        }
    },
}


@router.get(
    "/me",
    response_model=UserSchema,
    summary="Get the current user",
    description="Return the authenticated user's public account information.",
    responses={
        status.HTTP_404_NOT_FOUND: NOT_FOUND_RESPONSE,
        status.HTTP_500_INTERNAL_SERVER_ERROR: INTERNAL_SERVER_ERROR_RESPONSE,
    },
)
async def read_users_me(
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    """Return the account associated with the current access token."""
    return current_user