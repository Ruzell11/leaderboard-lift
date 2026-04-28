# app/controllers/auth_controller.py

from fastapi import HTTPException, Response, Cookie
from app.services.auth_services import signup_user, login_user, refresh_access_token, logout_user
from app.schemas.auth import  AuthRequest, RefreshRequest

COOKIE_KEY = "refresh_token"
COOKIE_MAX_AGE = 60 * 60 * 24 * 7  # 7 days in seconds


def _set_refresh_cookie(response: Response, token: str):
    response.set_cookie(
        key=COOKIE_KEY,
        value=token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=COOKIE_MAX_AGE,
    )


def _clear_refresh_cookie(response: Response):
    response.delete_cookie(key=COOKIE_KEY)


async def signup_controller(db, body: AuthRequest, response: Response):
    try:
        result = await signup_user(db, body)
        _set_refresh_cookie(response, result["refresh_token"])

        return {
            "message": "User created successfully",
            "access_token": result["access_token"],
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def login_controller(db, body: AuthRequest, response: Response):
    try:
        result = await login_user(db, body)
        _set_refresh_cookie(response, result["refresh_token"])

        return {
            "message": "Login successful",
            "access_token": result["access_token"],
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


async def refresh_controller(db, response: Response, refresh_token: str = Cookie(None)):
    try:
        if not refresh_token:
            raise HTTPException(status_code=401, detail="No refresh token provided")

        result = await refresh_access_token(db, refresh_token)
        _set_refresh_cookie(response, result["refresh_token"])

        return {
            "message": "Token refreshed",
            "access_token": result["access_token"],
            "token_type": "bearer"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


async def logout_controller(db, response: Response, refresh_token: str = Cookie(None)):
    try:
        if refresh_token:
            await logout_user(db, refresh_token)

        _clear_refresh_cookie(response)
        return {"message": "Logged out successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))