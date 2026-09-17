from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_current_user, get_user_service
from core.exceptions import UserAlreadyExistsError, UserNotFoundError
from domain.users.dto import CreateUserDTO, UpdateUserDTO, UserDTO
from domain.users.models import User
from domain.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]


@router.post(
    "/register",
    summary="Создание пользователя",
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: CreateUserDTO,
    user_service: UserServiceDep,
):
    try:
        return await user_service.create_user(user_data)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )


@router.get(
    "/email/{email}",
    summary="Пользователь по email",
    response_model=UserDTO,
)
async def get_user_by_email(
    email: str,
    current_user: CurrentUserDep,
    user_service: UserServiceDep,
):
    try:
        return await user_service.get_user_by_email(email)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


@router.get(
    "/{user_id}",
    summary="Пользователь по id",
    response_model=UserDTO,
)
async def get_user_by_id(
    user_id: int,
    current_user: CurrentUserDep,
    user_service: UserServiceDep,
):
    try:
        return await user_service.get_user_by_id(user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


@router.put(
    "",
    summary="Обновить данные текущего пользователя",
    response_model=UserDTO,
)
async def update_user(
    update_data: UpdateUserDTO,
    current_user: CurrentUserDep,
    user_service: UserServiceDep,
):
    try:
        return await user_service.update_user(current_user.id, update_data)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
