from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from core.constants import (
    USER_EMAIL_MAX_LEN,
    USER_HASHED_PASSWORD_MAX_LEN,
    USER_USERNAME_MAX_LEN,
)
from core.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(USER_EMAIL_MAX_LEN),
        unique=True,
        index=True,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        String(USER_USERNAME_MAX_LEN),
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(USER_HASHED_PASSWORD_MAX_LEN),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r} username={self.username!r}>"
