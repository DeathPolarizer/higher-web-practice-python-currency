from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import UserAlreadyExistsError, UserNotFoundError
from domain.users.dto import CreateUserDTO, UpdateUserDTO
from domain.users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User:
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user is None:
            raise UserNotFoundError(f"User with email {email} not found")
        return user

    async def get_user_by_id(self, id: int) -> User:
        result = await self.db.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        if user is None:
            raise UserNotFoundError(f"User with id {id} not found")
        return user

    async def create_user(self, user_dto: CreateUserDTO) -> User:
        result = await self.db.execute(
            select(User).where(User.email == user_dto.email)
        )
        if result.scalar_one_or_none() is not None:
            raise UserAlreadyExistsError(
                f"User with email {user_dto.email} already exists"
            )

        user = User(
            email=user_dto.email,
            username=user_dto.username,
            hashed_password=pwd_context.hash(user_dto.password),
        )
        self.db.add(user)
        await self.db.commit()
        return user

    async def update_user(
        self, user_id: int, update_dto: UpdateUserDTO
    ) -> User:
        user = await self.get_user_by_id(user_id)

        if update_dto.email is not None:
            user.email = update_dto.email
        if update_dto.username is not None:
            user.username = update_dto.username
        if update_dto.password is not None:
            user.hashed_password = pwd_context.hash(update_dto.password)

        await self.db.commit()
        return user
