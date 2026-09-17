from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateUserDTO(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserDTO(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserWithPasswordDTO(UserDTO):
    hashed_password: str


class UpdateUserDTO(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None
