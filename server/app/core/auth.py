# app/dependencies/auth.py

from fastapi import Depends, Header
from app.utils.jwt import decode_access_token


async def get_current_user(authorization: str = Header(...)) -> dict:
    if not authorization.startswith("Bearer "):
        raise Exception("Invalid authorization header")
    
    token = authorization.removeprefix("Bearer ")
    payload = decode_access_token(token)  # raises if expired or invalid
    return payload 


# Usage on any protected route:
# @router.get("/me")
# async def me(user: dict = Depends(get_current_user)):
#     return {"user_id": user["user_id"]}