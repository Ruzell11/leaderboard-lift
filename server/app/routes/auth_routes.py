# app/routers/auth_router.py

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.database import get_db
from app.controller.auth_controller import signup_controller, login_controller, refresh_controller, logout_controller
from app.schemas.auth import  AuthRequest, RefreshRequest

router = APIRouter(prefix="/api/auth", tags=["auth"])



@router.post("/signup")
async def signup(body: AuthRequest, response: Response,db: AsyncSession = Depends(get_db)):
    return await signup_controller(db, body, response)


@router.post("/login")
async def login(body: AuthRequest, response: Response, db: AsyncSession = Depends(get_db)):
    return await login_controller(db, body, response)


@router.post("/refresh")
async def refresh(body: RefreshRequest, response: Response, db: AsyncSession = Depends(get_db)):
    return await refresh_controller(db, response, body.refresh_token)


@router.post("/logout")
async def logout(body: RefreshRequest, response: Response, db: AsyncSession = Depends(get_db)):
    await logout_controller(db, response, body.refresh_token)
    return {"message": "Logged out successfully"}