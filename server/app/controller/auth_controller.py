
from fastapi import HTTPException
from app.services.auth_services import signup_user, login_user

async def signup_controller(db, email: str, password: str):
    try:
        user = await signup_user(db, email, password)

        return {
            "message": "User created successfully",
            "user": {
                "id": user.id,
                "email": user.email
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

async def login_controller(db, email: str, password: str):
    try:
        result = await login_user(db, email, password)

        return {
            "message": "Login successful",
            "access_token": result["access_token"],
            "user_id": result["user_id"],
            "token_type": "bearer"
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))