
from pydantic import BaseModel, EmailStr
from datetime import datetime

class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: int 
    email: str
    created_at: datetime
    class Config:
        from_attributes = True

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
