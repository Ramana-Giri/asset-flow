from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.core.responses import success
from app.repositories.user_repository import UserRepository
from app.repositories.activity_log_repository import ActivityLogRepository
from app.services.auth_service import AuthService
from app.services.activity_log_service import ActivityLogService
from app.schemas.auth import (
    SignupRequest, LoginRequest, LoginResponse,
    ForgotPasswordRequest, ResetPasswordRequest,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db, UserRepository(db), ActivityLogService(ActivityLogRepository(db)))


@router.post("/signup")
async def signup(payload: SignupRequest, request: Request, service: AuthService = Depends(get_auth_service)):
    user = await service.signup(payload.name, payload.email, payload.password, ip_address=request.client.host)
    return success(data={"id": user.id, "email": user.email}, message="Account created")


@router.post("/login", response_model=None)
async def login(payload: LoginRequest, request: Request, service: AuthService = Depends(get_auth_service)):
    result = await service.login(
        payload.email, payload.password, ip_address=request.client.host, user_agent=request.headers.get("user-agent")
    )
    return success(data=result, message="Login successful")


@router.post("/refresh")
async def refresh_session(service: AuthService = Depends(get_auth_service), user=Depends(get_current_user)):
    # Session-based auth simply re-validates; no separate refresh token exists.
    return success(data={"user_id": user.id}, message="Session is active")


@router.post("/logout")
async def logout(session_token: str, service: AuthService = Depends(get_auth_service)):
    await service.logout(session_token)
    return success(message="Logged out")


@router.post("/forgot-password")
async def forgot_password(payload: ForgotPasswordRequest, service: AuthService = Depends(get_auth_service)):
    await service.forgot_password(payload.email)
    return success(message="If that email exists, a reset link has been sent")


@router.post("/reset-password")
async def reset_password(payload: ResetPasswordRequest, service: AuthService = Depends(get_auth_service)):
    await service.reset_password(payload.token, payload.new_password)
    return success(message="Password reset successful")


@router.get("/session")
async def validate_session(user=Depends(get_current_user)):
    return success(data={"id": user.id, "email": user.email, "role": user.role}, message="Session valid")