# app/utils/jwt.py

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import secrets

SECRET_KEY = "your-secret-key"       # move to env var
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 15     # short-lived
REFRESH_TOKEN_EXPIRE_DAYS = 7        # long-lived


def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["type"] = "access"
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token() -> str:
    """Opaque random token — stored in DB, not a JWT."""
    return secrets.token_urlsafe(64)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise JWTError("Not an access token")
        return payload
    except JWTError:
        raise Exception("Invalid or expired access token")