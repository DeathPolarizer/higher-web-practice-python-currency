from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from core.config import settings
from core.exceptions import CredentialsError, UserNotFoundError
from domain.auth.dto import Token, TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    ALGORITHM = settings.ALGORITHM
    SECRET_KEY = settings.SECRET_KEY

    def __init__(self, user_service):
        self.user_service = user_service

    def _create_token(self, payload: dict, expires_delta: timedelta) -> str:
        data = payload.copy()
        data["exp"] = datetime.now(timezone.utc) + expires_delta
        return jwt.encode(data, self.SECRET_KEY, algorithm=self.ALGORITHM)

    async def login(self, email: str, password: str) -> Token:
        try:
            user = await self.user_service.get_user_by_email(email)
        except UserNotFoundError:
            raise CredentialsError("Invalid credentials")

        if not pwd_context.verify(password, user.hashed_password):
            raise CredentialsError("Invalid credentials")

        access_token = self._create_token(
            {"user_id": user.id, "email": user.email, "type": "access"},
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = self._create_token(
            {"user_id": user.id, "email": user.email, "type": "refresh"},
            timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return Token(access_token=access_token, refresh_token=refresh_token)

    async def refresh_tokens(self, refresh_token: str) -> Token:
        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload.get("type") != "refresh":
                raise CredentialsError("Invalid token type")
            user = await self.user_service.get_user_by_id(payload["user_id"])
        except (JWTError, KeyError, UserNotFoundError):
            raise CredentialsError("Invalid token")

        access_token = self._create_token(
            {"user_id": user.id, "email": user.email, "type": "access"},
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        new_refresh = self._create_token(
            {"user_id": user.id, "email": user.email, "type": "refresh"},
            timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return Token(access_token=access_token, refresh_token=new_refresh)

    def verify_access_token(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload.get("type") != "access":
                raise CredentialsError("Invalid token type")
            return TokenPayload(
                user_id=payload["user_id"],
                email=payload["email"],
                exp=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
            )
        except (JWTError, KeyError):
            raise CredentialsError("Invalid token")
