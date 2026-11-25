from datetime import timedelta

from app.core.config import settings
from app.core.dependencies import get_db
from app.core.security import create_access_token
from app.crud.user import authenticate_user, create_user, get_user_by_username
from app.schemas.user import ErrorResponse, Token, User, UserCreate
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["Authentication"])

BAD_REQUEST_RESPONSE = {
    "model": ErrorResponse,
    "description": "The request could not be completed because it was invalid.",
    "content": {
        "application/json": {
            "example": {"detail": "Username already registered"},
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


@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
    description="Create a new user account with a unique username and email address.",
    responses={
        status.HTTP_400_BAD_REQUEST: BAD_REQUEST_RESPONSE,
        status.HTTP_500_INTERNAL_SERVER_ERROR: INTERNAL_SERVER_ERROR_RESPONSE,
    },
)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),  # noqa: B008
):
    """Create a user unless the username is already registered."""
    existing_user = await get_user_by_username(db, user_in.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    user = await create_user(db, user_in)
    return user


UNAUTHORIZED_RESPONSE = {
    "model": ErrorResponse,
    "description": "The supplied credentials are invalid.",
    "content": {
        "application/json": {
            "example": {"detail": "Incorrect username or password"},
        }
    },
}


@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate a user",
    description="Exchange a username and password for a bearer access token.",
    responses={
        status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED_RESPONSE,
        status.HTTP_500_INTERNAL_SERVER_ERROR: INTERNAL_SERVER_ERROR_RESPONSE,
    },
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/x-www-form-urlencoded": {
                    "schema": {
                        "type": "object",
                        "required": ["username", "password"],
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "Username associated with the account.",
                                "example": "jane_doe",
                            },
                            "password": {
                                "type": "string",
                                "format": "password",
                                "description": "Password associated with the account.",
                                "example": "A-secure-password123",
                            },
                        },
                    },
                    "examples": {
                        "valid_credentials": {
                            "summary": "Valid login credentials",
                            "value": {
                                "username": "jane_doe",
                                "password": "A-secure-password123",
                            },
                        }
                    },
                }
            },
        }
    },
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa: B008
    db: AsyncSession = Depends(get_db),  # noqa: B008
):
    """Validate credentials and issue an access token."""
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}