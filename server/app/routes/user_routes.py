from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.user_repository import get_all_users

router = APIRouter(prefix="/api/users", tags=["users"])



@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await get_all_users(db)
    return users