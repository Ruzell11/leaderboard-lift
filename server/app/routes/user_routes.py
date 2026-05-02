from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.user_repository import (
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user
)
from app.core.auth import get_current_user  # 👈 you must have this
from app.models.user import User

router = APIRouter(prefix="/api/users", tags=["users"])


# 📄 Get all users (⚠️ restrict this if needed)
@router.get("/")
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_all_users(db)


# 🔍 Get user by ID (only self)
@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    user = await get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ✏️ Update user (only self)
@router.put("/{user_id}")
async def update_user_route(
    user_id: int,
    email: str | None = None,
    password: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    user = await update_user(db, user_id, email, password)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ❌ Delete user (only self)
@router.delete("/{user_id}")
async def delete_user_route(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    success = await delete_user(db, user_id)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}