from __future__ import annotations
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class SignupRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class LoginUserSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    role: str
    department_id: Optional[int] = None


class LoginResponse(BaseModel):
    session_token: str
    expires_at: datetime
    user: LoginUserSummary


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)


class LogoutRequest(BaseModel):
    session_token: Optional[str] = None


class SessionValidationResponse(BaseModel):
    valid: bool
    user: Optional[LoginUserSummary] = None
    expires_at: Optional[datetime] = None