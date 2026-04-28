# app/services/auth_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import get_user_by_email, create_user
from app.repositories.token_repository import (
    save_refresh_token,
    get_refresh_token,
    revoke_refresh_token,
)
from app.utils.hash import hash_password, verify_password
from app.utils.jwt import create_access_token, create_refresh_token, decode_access_token


def _token_response(user_id: str, refresh_token: str) -> dict:
    return {
        "access_token": create_access_token({"user_id": user_id}),
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# ✅ SIGNUP
async def signup_user(db: AsyncSession, email: str, password: str):
    existing_user = await get_user_by_email(db, email)
    if existing_user:
        raise Exception("Email already registered")

    hashed_password = hash_password(password)
    user = await create_user(db, email, hashed_password)

    refresh_token = create_refresh_token()
    await save_refresh_token(db, str(user.id), refresh_token)

    return _token_response(str(user.id), refresh_token)


# ✅ LOGIN
async def login_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)

    if not user or not verify_password(password, user.password):
        raise Exception("Invalid credentials")

    refresh_token = create_refresh_token()
    await save_refresh_token(db, str(user.id), refresh_token)

    return _token_response(str(user.id), refresh_token)


# ✅ REFRESH
async def refresh_access_token(db: AsyncSession, refresh_token: str):
    rt = await get_refresh_token(db, refresh_token)

    if not rt or not rt.is_valid:
        raise Exception("Invalid or expired refresh token")

    # Rotate: revoke old, issue new refresh token
    await revoke_refresh_token(db, refresh_token)
    new_refresh_token = create_refresh_token()
    await save_refresh_token(db, rt.user_id, new_refresh_token)

    return _token_response(rt.user_id, new_refresh_token)


# ✅ LOGOUT
async def logout_user(db: AsyncSession, refresh_token: str):
    await revoke_refresh_token(db, refresh_token)