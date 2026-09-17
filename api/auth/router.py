from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_auth_service
from core.exceptions import CredentialsError
from domain.auth.dto import LoginRequest, RefreshRequest, Token
from domain.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


@router.post(
    "/login",
    summary="Аутентификация пользователя",
    response_model=Token,
)
async def login(
    request: LoginRequest,
    auth_service: AuthServiceDep,
):
    try:
        return await auth_service.login(request.email, request.password)
    except CredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@router.post(
    "/refresh",
    summary="Обновление токена",
    response_model=Token,
)
async def refresh(
    request: RefreshRequest,
    auth_service: AuthServiceDep,
):
    try:
        return await auth_service.refresh_tokens(request.refresh_token)
    except CredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
