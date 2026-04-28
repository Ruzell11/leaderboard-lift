from pydantic import BaseModel, EmailStr

class AuthRequest(BaseModel):
    email: EmailStr
    password: str




class RefreshRequest(BaseModel):
    refresh_token: str