# app/routers/auth_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.database import get_db
from app.services.auth_services import (
    signup_user, login_user, refresh_access_token, logout_user
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


class AuthRequest(BaseModel):
    email: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/signup")
async def signup(body: AuthRequest, db: AsyncSession = Depends(get_db)):
    return await signup_user(db, body.email, body.password)


@router.post("/login")
async def login(body: AuthRequest, db: AsyncSession = Depends(get_db)):
    return await login_user(db, body.email, body.password)


@router.post("/refresh")
async def refresh(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    return await refresh_access_token(db, body.refresh_token)


@router.post("/logout")
async def logout(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    await logout_user(db, body.refresh_token)
    return {"message": "Logged out successfully"}