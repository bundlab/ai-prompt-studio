from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.schemas.user import UserCreate, User
from app.crud.user import create_user
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
