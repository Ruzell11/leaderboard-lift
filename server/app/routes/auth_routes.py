# app/routers/auth_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.database import get_db
from app.controller.auth_controller import signup_controller, login_controller, refresh_controller, logout_controller
from app.schemas.auth import  AuthRequest, RefreshRequest
router = APIRouter(prefix="/api/auth", tags=["auth"])



@router.post("/signup")
async def signup(body: AuthRequest, db: AsyncSession = Depends(get_db)):
    return await signup_controller(db, body)


@router.post("/login")
async def login(body: AuthRequest, db: AsyncSession = Depends(get_db)):
    return await login_controller(db, body.email, body.password)


@router.post("/refresh")
async def refresh(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    return await refresh_controller(db, body.refresh_token)


@router.post("/logout")
async def logout(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    await logout_controller(db, body.refresh_token)
    return {"message": "Logged out successfully"}