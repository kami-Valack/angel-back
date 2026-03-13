# Schemas for requests and responses (Pydantic models)
from pydantic import BaseModel
from typing import Optional, List

class UserSchema(BaseModel):
    id: str
    name: str
    email: str
    bio: Optional[str]
    avatar: Optional[str]
    createdAt: Optional[str]
    updatedAt: Optional[str]
    stats: Optional[dict]

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str
