from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from core.exceptions import CredentialsError, UserNotFoundError
from domain.auth.service import AuthService
from domain.currency.service import CurrencyService
from domain.users.models import User
from domain.users.service import UserService

bearer_scheme = HTTPBearer()


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


async def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(user_service)


async def get_currency_service(
    db: AsyncSession = Depends(get_db),
) -> CurrencyService:
    return CurrencyService(db)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = auth_service.verify_access_token(credentials.credentials)
        user = await UserService(db).get_user_by_id(payload.user_id)
        return user
    except (CredentialsError, UserNotFoundError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
